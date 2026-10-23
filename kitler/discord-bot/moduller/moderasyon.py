"""Moderasyon: ban/at/sustur/temizle/uyar komutları, link engeli, spam susturma. Uyarılar veriler/uyarilar.json'da."""
import datetime as dt
import json
import re
import time
from collections import defaultdict, deque
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

LINK = re.compile(r"(https?://|www\.|discord\.gg/|discord(app)?\.com/invite/)\S+", re.IGNORECASE)
VERI = Path("veriler/uyarilar.json")


def link_var(metin: str) -> bool:
    return bool(LINK.search(metin or ""))


class SpamSayaci:
    """Bir kişinin son `saniye` içindeki mesaj sayısı `mesaj`ı aşarsa True."""

    def __init__(self, mesaj: int, saniye: float):
        self.mesaj, self.saniye = mesaj, saniye
        self.gecmis: dict[int, deque] = defaultdict(deque)

    def ekle(self, uye_id: int, an: float | None = None) -> bool:
        an = time.monotonic() if an is None else an
        q = self.gecmis[uye_id]
        q.append(an)
        while q and an - q[0] > self.saniye:
            q.popleft()
        if len(q) > self.mesaj:
            q.clear()
            return True
        return False


class Uyarilar:
    def __init__(self, yol: Path = VERI):
        self.yol = yol
        self.veri: dict[str, list[dict]] = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}

    def ekle(self, uye_id: int, sebep: str, yetkili: str) -> int:
        liste = self.veri.setdefault(str(uye_id), [])
        liste.append({"sebep": sebep, "yetkili": yetkili, "zaman": dt.datetime.now().isoformat(timespec="minutes")})
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        self.yol.write_text(json.dumps(self.veri, ensure_ascii=False, indent=1), encoding="utf-8")
        return len(liste)

    def listele(self, uye_id: int) -> list[dict]:
        return self.veri.get(str(uye_id), [])


class Moderasyon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = bot.ayar["moduller"]["moderasyon"]
        s = self.a.get("spam") or {}
        self.spam = SpamSayaci(s.get("mesaj", 5), s.get("saniye", 5))
        self.uyarilar = Uyarilar()

    def yetkili_mi(self, uye) -> bool:
        if not isinstance(uye, discord.Member):
            return False
        return uye.guild_permissions.administrator or any(r.id == self.a["yetkili_rol_id"] for r in uye.roles)

    async def interaction_check(self, e: discord.Interaction) -> bool:
        if self.yetkili_mi(e.user):
            return True
        await e.response.send_message("Bu komut için yetkin yok.", ephemeral=True)
        return False

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.bot or not m.guild or self.yetkili_mi(m.author):
            return
        if self.a.get("link_engeli") and link_var(m.content):
            await m.delete()
            await m.channel.send(f"{m.author.mention} bu sunucuda bağlantı paylaşmak yasak.", delete_after=5)
            return await self.bot.logla("Bağlantı silindi", f"{m.author.mention} #{m.channel.name}: {m.content[:300]}")
        if self.spam.ekle(m.author.id):
            dakika = (self.a.get("spam") or {}).get("sustur_dakika", 10)
            await m.author.timeout(dt.timedelta(minutes=dakika), reason="Spam")
            await m.channel.send(f"{m.author.mention} spam yüzünden {dakika} dk susturuldu.", delete_after=10)
            await self.bot.logla("Spam susturması", f"{m.author.mention} {dakika} dk")

    @app_commands.command(name="ban", description="Üyeyi sunucudan yasaklar")
    async def ban(self, e: discord.Interaction, uye: discord.Member, sebep: str = "Belirtilmedi"):
        await uye.ban(reason=f"{sebep} — {e.user}")
        await self._bitir(e, "Yasaklandı", f"{uye} — {sebep}")

    @app_commands.command(name="at", description="Üyeyi sunucudan atar")
    async def at(self, e: discord.Interaction, uye: discord.Member, sebep: str = "Belirtilmedi"):
        await uye.kick(reason=f"{sebep} — {e.user}")
        await self._bitir(e, "Atıldı", f"{uye} — {sebep}")

    @app_commands.command(name="sustur", description="Üyeyi belirli dakika susturur")
    async def sustur(self, e: discord.Interaction, uye: discord.Member, dakika: app_commands.Range[int, 1, 40320],
                     sebep: str = "Belirtilmedi"):
        await uye.timeout(dt.timedelta(minutes=dakika), reason=f"{sebep} — {e.user}")
        await self._bitir(e, "Susturuldu", f"{uye.mention} {dakika} dk — {sebep}")

    @app_commands.command(name="temizle", description="Kanaldaki son mesajları siler (en çok 100)")
    async def temizle(self, e: discord.Interaction, adet: app_commands.Range[int, 1, 100]):
        await e.response.defer(ephemeral=True)
        silinen = await e.channel.purge(limit=adet)
        await e.followup.send(f"{len(silinen)} mesaj silindi.", ephemeral=True)
        await self.bot.logla("Temizlik", f"#{e.channel.name}: {len(silinen)} mesaj — {e.user.mention}")

    @app_commands.command(name="uyar", description="Üyeye uyarı verir; limitte 60 dk susturur")
    async def uyar(self, e: discord.Interaction, uye: discord.Member, sebep: str):
        sayi = self.uyarilar.ekle(uye.id, sebep, str(e.user))
        ek = ""
        if sayi >= self.a.get("uyari_limiti", 3):
            await uye.timeout(dt.timedelta(minutes=60), reason=f"Uyarı limiti ({sayi})")
            ek = " Uyarı limitine ulaştı, 60 dk susturuldu."
        await self._bitir(e, "Uyarı", f"{uye.mention} ({sayi}. uyarı) — {sebep}.{ek}")

    @app_commands.command(name="uyarilar", description="Üyenin uyarı geçmişi")
    async def uyarilar_komut(self, e: discord.Interaction, uye: discord.Member):
        liste = self.uyarilar.listele(uye.id)
        metin = "\n".join(f"{i}. {u['zaman']} — {u['sebep']} ({u['yetkili']})" for i, u in enumerate(liste, 1))
        await e.response.send_message(metin or "Uyarı yok.", ephemeral=True)

    async def _bitir(self, e: discord.Interaction, baslik: str, metin: str):
        await e.response.send_message(f"{baslik}: {metin}", ephemeral=True)
        await self.bot.logla(baslik, f"{metin} — {e.user.mention}")


async def setup(bot):
    await bot.add_cog(Moderasyon(bot))
