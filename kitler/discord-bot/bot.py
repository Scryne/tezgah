"""Tezgah Discord botu. Çalıştırma: python bot.py (ayrıntı KURULUM.md)."""
import logging
import os
import socket
import time

import aiohttp
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

    async def login(self, token: str):
        # Yalnız IPv4: AAAA kaydı olmayan ağlarda DNS her yeni bağlantıda ~12 sn bekliyor ve Discord'un 3 sn yanıt
        # sınırı kaçıyor (2026-10-24 testi: AF_UNSPEC 11,6 sn, AF_INET 0,02 sn). ayar.yaml'da yalniz_ipv4: false ile kapanır.
        if self.ayar.get("yalniz_ipv4", True):
            self.http.connector = aiohttp.TCPConnector(family=socket.AF_INET, ttl_dns_cache=300, limit=0)
        await super().login(token)

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
    # Açılıştaki geçici bağlantı hatasında discord.py yeniden bağlanmadan çökebiliyor (gateway 503, 2026-10-24 testi):
    # bot kendini yeniden başlatır. Token ve izin hataları düzelmeyeceği için hemen durur.
    for deneme in range(1, 11):
        try:
            Bot(ayar).run(token, log_handler=None)
            return
        except discord.LoginFailure:
            raise SystemExit("Token geçersiz: Developer Portal > Bot > Reset Token ile yenisini al, .env'e yaz.") from None
        except discord.PrivilegedIntentsRequired:
            raise SystemExit("Developer Portal > Bot sayfasında Server Members ve Message Content intent'lerini aç.") from None
        except KeyboardInterrupt:
            return
        except Exception:
            bekle = min(60, 5 * deneme)
            log.exception("Bağlantı koptu, %d sn sonra yeniden deneniyor (%d/10)", bekle, deneme)
            time.sleep(bekle)
    raise SystemExit("10 denemede bağlanılamadı; internet bağlantısını kontrol et.")


if __name__ == "__main__":
    main()
