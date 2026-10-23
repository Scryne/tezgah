"""Test sunucusunu bot üzerinden hazırlar: roller, kategori, kanallar; kimlikleri ayar.yaml'a yazar.
Kullanım: python scripts/test_sunucu_kur.py <klasör>  (klasörde .env/DISCORD_TOKEN; bot yalnız bir sunucuda olmalı)
Aynı adlı rol/kanal varsa yenisini açmaz."""
import sys
from pathlib import Path

import discord
import yaml
from dotenv import dotenv_values

KLASOR = Path(sys.argv[1])
KIT = Path(__file__).resolve().parents[1] / "kitler" / "discord-bot"
TOKEN = dotenv_values(KLASOR / ".env")["DISCORD_TOKEN"]

client = discord.Client(intents=discord.Intents.default())


async def rol(g, ad):
    return discord.utils.get(g.roles, name=ad) or await g.create_role(name=ad, reason="Tezgah test")


async def kanal(g, ad, kategori=None):
    return discord.utils.get(g.text_channels, name=ad) or await g.create_text_channel(ad, category=kategori)


@client.event
async def on_ready():
    try:
        if len(client.guilds) != 1:
            print(f"HATA: bot {len(client.guilds)} sunucuda; tek test sunucusunda olmalı")
            return
        g = client.guilds[0]
        destek_rol, kayitsiz, uye, mod = [await rol(g, a) for a in ("Destek Ekibi", "Kayıtsız", "Üye", "Moderatör")]
        kategori = discord.utils.get(g.categories, name="Destek Talepleri") or await g.create_category("Destek Talepleri")
        log, destek, kayit, hosgeldin = [await kanal(g, a) for a in ("bot-log", "destek", "kayit", "hosgeldin")]
        ayar = yaml.safe_load((KIT / "ayar.ornek.yaml").read_text(encoding="utf-8"))
        ayar["sunucu_id"], ayar["log_kanal_id"] = g.id, log.id
        m = ayar["moduller"]
        m["ticket"].update(kategori_id=kategori.id, destek_rol_id=destek_rol.id)
        m["kayit"].update(kayitsiz_rol_id=kayitsiz.id, uye_rol_id=uye.id, hosgeldin_kanal_id=hosgeldin.id)
        m["moderasyon"].update(yetkili_rol_id=mod.id)
        (KLASOR / "ayar.yaml").write_text(yaml.safe_dump(ayar, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"Sunucu: {g.name} · kanallar: #{destek.name} #{kayit.name} #{hosgeldin.name} #{log.name} · ayar.yaml yazıldı")
    finally:
        await client.close()


client.run(TOKEN, log_handler=None)
