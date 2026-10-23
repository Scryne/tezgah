"""Kayıt: yeni gelen 'kayıtsız' rolü alır; panel düğmesi isim/yaş formu açar, takma ad ve üye rolü verilir."""
import ayar as ayar_mod
import discord
from discord import app_commands
from discord.ext import commands


def takma_ad(sablon: str, isim: str, yas: str) -> str:
    isim = " ".join(w.capitalize() for w in isim.split())
    return sablon.format(isim=isim, yas=yas)[:32]  # Discord takma ad sınırı


def yas_gecerli(yas: str, alt_sinir: int) -> bool:
    return yas.strip().isdigit() and alt_sinir <= int(yas) <= 99


class Form(discord.ui.Modal, title="Kayıt"):
    isim = discord.ui.TextInput(label="İsmin", min_length=2, max_length=20)
    yas = discord.ui.TextInput(label="Yaşın", min_length=1, max_length=2)

    def __init__(self, cog: "Kayit"):
        super().__init__()
        self.cog = cog

    async def on_submit(self, e: discord.Interaction):
        await self.cog.kaydet(e, str(self.isim), str(self.yas))


class Panel(discord.ui.View):
    def __init__(self, cog: "Kayit"):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Kayıt Ol", style=discord.ButtonStyle.blurple, emoji="📝", custom_id="tezgah:kayit:ac")
    async def ac(self, e: discord.Interaction, _):
        await e.response.send_modal(Form(self.cog))


class Kayit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = bot.ayar["moduller"]["kayit"]
        bot.add_view(Panel(self))

    @commands.Cog.listener()
    async def on_member_join(self, uye: discord.Member):
        if uye.bot:
            return
        rol = uye.guild.get_role(self.a["kayitsiz_rol_id"])
        if rol:
            await uye.add_roles(rol, reason="Yeni üye: kayıtsız")
        kanal = uye.guild.get_channel(self.a["hosgeldin_kanal_id"])
        if kanal:
            await kanal.send(self.a.get("hosgeldin_mesaji", "{kullanici} hoş geldin!").format(kullanici=uye.mention))

    async def kaydet(self, e: discord.Interaction, isim: str, yas: str):
        if not yas_gecerli(yas, self.a.get("yas_alt_sinir", 13)):
            return await e.response.send_message(
                f"Yaş {self.a.get('yas_alt_sinir', 13)} ile 99 arasında bir sayı olmalı.", ephemeral=True)
        uye, sunucu = e.user, e.guild
        ad = takma_ad(self.a.get("takma_ad", "{isim} | {yas}"), isim, yas)
        try:
            await uye.edit(nick=ad, reason="Kayıt")
        except discord.Forbidden:
            pass  # sunucu sahibinin takma adı botla değişmez; rol yine verilir
        kayitsiz, uye_rol = sunucu.get_role(self.a["kayitsiz_rol_id"]), sunucu.get_role(self.a["uye_rol_id"])
        if kayitsiz in uye.roles:
            await uye.remove_roles(kayitsiz, reason="Kayıt")
        if uye_rol:
            await uye.add_roles(uye_rol, reason="Kayıt")
        await e.response.send_message(f"Kaydın tamam, hoş geldin {ad}!", ephemeral=True)
        await self.bot.logla("Kayıt", f"{uye.mention} → {ad}")

    @app_commands.command(name="kayit-panel", description="Bu kanala kayıt panelini koyar")
    @app_commands.default_permissions(manage_guild=True)
    async def panel(self, e: discord.Interaction):
        gom = discord.Embed(title="Kayıt", description="Sunucuya erişmek için aşağıdaki düğmeyle kaydını tamamla.",
                            color=ayar_mod.renk(self.bot.ayar))
        await e.channel.send(embed=gom, view=Panel(self))
        await e.response.send_message("Panel kuruldu.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Kayit(bot))
