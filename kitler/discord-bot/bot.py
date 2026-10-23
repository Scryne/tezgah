"""Tezgah Discord botu. Çalıştırma: python bot.py (ayrıntı KURULUM.md)."""
import logging
import os

import ayar as ayar_mod
import discord
from discord.ext import commands
from dotenv import load_dotenv

log = logging.getLogger("bot")
MODULLER = {"ticket": "moduller.ticket", "kayit": "moduller.kayit", "moderasyon": "moduller.moderasyon"}


class Bot(commands.Bot):
    def __init__(self, ayar: dict):
        intents = discord.Intents.default()
        intents.members = True  # kayıt: sunucuya giriş olayı
        intents.message_content = bool(ayar["moduller"].get("moderasyon", {}).get("acik"))  # link engeli
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.ayar = ayar

    async def setup_hook(self):
        for ad, yol in MODULLER.items():
            if (self.ayar["moduller"].get(ad) or {}).get("acik"):
                await self.load_extension(yol)
        sunucu = discord.Object(id=self.ayar["sunucu_id"])
        self.tree.copy_global_to(guild=sunucu)
        komutlar = await self.tree.sync(guild=sunucu)
        log.info("%d komut sunucuya yüklendi", len(komutlar))

    async def on_ready(self):
        log.info("Bağlandı: %s", self.user)

    async def logla(self, baslik: str, aciklama: str, dosya: discord.File | None = None):
        kanal = self.get_channel(self.ayar["log_kanal_id"])
        if kanal:
            gom = discord.Embed(title=baslik, description=aciklama[:4000], color=ayar_mod.renk(self.ayar))
            await kanal.send(embed=gom, file=dosya) if dosya else await kanal.send(embed=gom)


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit(".env dosyasında DISCORD_TOKEN yok (.env.ornek'e bak).")
    try:
        ayar = ayar_mod.oku()
    except ayar_mod.AyarHatasi as e:
        raise SystemExit(str(e)) from None
    Bot(ayar).run(token, log_handler=None)


if __name__ == "__main__":
    main()
