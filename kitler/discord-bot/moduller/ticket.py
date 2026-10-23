"""Destek talebi: panel düğmesi özel kanal açar, kapatınca döküm log kanalına düşer ve kanal silinir."""
import asyncio
import io
import re

import ayar as ayar_mod
import discord
from discord import app_commands
from discord.ext import commands

ETIKET = "tezgah-ticket:"  # kanal konusunda sahibin kimliği; yeniden başlatmada da bulunur


def kanal_adi(kullanici_adi: str) -> str:
    temiz = re.sub(r"[^a-z0-9-]+", "-", kullanici_adi.lower()).strip("-") or "kullanici"
    return f"destek-{temiz}"[:90]


def dokum(mesajlar: list[tuple[str, str, str]]) -> str:
    """(zaman, yazar, içerik) listesinden düz metin döküm."""
    return "\n".join(f"[{z}] {y}: {i}" for z, y, i in mesajlar) or "(mesaj yok)"


class Panel(discord.ui.View):
    def __init__(self, cog: "Ticket"):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Destek Talebi Aç", style=discord.ButtonStyle.green, emoji="🎫", custom_id="tezgah:ticket:ac")
    async def ac(self, etkilesim: discord.Interaction, _):
        await self.cog.ac(etkilesim)


class Kapat(discord.ui.View):
    def __init__(self, cog: "Ticket"):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Talebi Kapat", style=discord.ButtonStyle.red, emoji="🔒", custom_id="tezgah:ticket:kapat")
    async def kapat(self, etkilesim: discord.Interaction, _):
        await self.cog.kapat(etkilesim)


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = bot.ayar["moduller"]["ticket"]
        bot.add_view(Panel(self))  # kalıcı düğmeler: bot yeniden başlasa da çalışır
        bot.add_view(Kapat(self))

    def _acik_talepler(self, sunucu: discord.Guild, uye_id: int) -> list[discord.TextChannel]:
        kategori = sunucu.get_channel(self.a["kategori_id"])
        kanallar = kategori.text_channels if isinstance(kategori, discord.CategoryChannel) else []
        return [k for k in kanallar if (k.topic or "") == f"{ETIKET}{uye_id}"]

    async def ac(self, e: discord.Interaction):
        sunucu, uye = e.guild, e.user
        acik = self._acik_talepler(sunucu, uye.id)
        if len(acik) >= self.a.get("kisi_basi_limit", 1):
            return await e.response.send_message(f"Zaten açık bir talebin var: {acik[0].mention}", ephemeral=True)
        kategori = sunucu.get_channel(self.a["kategori_id"])
        destek = sunucu.get_role(self.a["destek_rol_id"])
        izinler = {
            sunucu.default_role: discord.PermissionOverwrite(view_channel=False),
            uye: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            sunucu.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        }
        if destek:
            izinler[destek] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        kanal = await sunucu.create_text_channel(kanal_adi(uye.name), category=kategori, overwrites=izinler,
                                                 topic=f"{ETIKET}{uye.id}")
        await kanal.send(self.a.get("karsilama", "{kullanici}").format(kullanici=uye.mention)
                         + (f" {destek.mention}" if destek else ""), view=Kapat(self))
        await e.response.send_message(f"Talebin açıldı: {kanal.mention}", ephemeral=True)
        await self.bot.logla("Talep açıldı", f"{uye.mention} → {kanal.mention}")

    async def kapat(self, e: discord.Interaction):
        kanal = e.channel
        sahip = (kanal.topic or "").removeprefix(ETIKET)
        destek = e.guild.get_role(self.a["destek_rol_id"])
        if str(e.user.id) != sahip and destek not in getattr(e.user, "roles", []):
            return await e.response.send_message("Bu talebi yalnız sahibi ya da destek ekibi kapatabilir.", ephemeral=True)
        await e.response.send_message("Talep 5 saniye içinde kapanıyor, döküm kaydedildi.")
        mesajlar = [(m.created_at.strftime("%Y-%m-%d %H:%M"), m.author.display_name, m.clean_content)
                    async for m in kanal.history(limit=None, oldest_first=True)]
        dosya = discord.File(io.BytesIO(dokum(mesajlar).encode("utf-8")), filename=f"{kanal.name}.txt")
        await self.bot.logla("Talep kapandı", f"{kanal.name} — kapatan {e.user.mention}", dosya)
        await asyncio.sleep(5)
        await kanal.delete(reason=f"Talep kapatıldı: {e.user}")

    @app_commands.command(name="ticket-panel", description="Bu kanala destek talebi panelini koyar")
    @app_commands.default_permissions(manage_guild=True)
    async def panel(self, e: discord.Interaction):
        gom = discord.Embed(title=self.a.get("panel_baslik", "Destek"), description=self.a.get("panel_metin", ""),
                            color=ayar_mod.renk(self.bot.ayar))
        await e.channel.send(embed=gom, view=Panel(self))
        await e.response.send_message("Panel kuruldu.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Ticket(bot))
