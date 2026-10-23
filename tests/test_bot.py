import asyncio
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

from tezgah.bot import KIT, paketle

sys.path.insert(0, str(KIT))
import ayar as kit_ayar
from moduller.kayit import takma_ad, yas_gecerli
from moduller.moderasyon import SpamSayaci, Uyarilar, link_var
from moduller.ticket import dokum, kanal_adi


def dolu_ayar():
    a = yaml.safe_load((KIT / "ayar.ornek.yaml").read_text(encoding="utf-8"))
    sayac = iter(range(100, 200))
    a["sunucu_id"], a["log_kanal_id"] = next(sayac), next(sayac)
    for m in a["moduller"].values():
        for k in m:
            if k.endswith("_id"):
                m[k] = next(sayac)
    return a


def test_ornek_ayar_bos_kimlikleri_tek_tek_soyler():
    a = yaml.safe_load((KIT / "ayar.ornek.yaml").read_text(encoding="utf-8"))
    with pytest.raises(kit_ayar.AyarHatasi) as h:
        kit_ayar.dogrula(a)
    for alan in ("sunucu_id", "moduller.ticket.kategori_id", "moduller.kayit.uye_rol_id", "moduller.moderasyon.yetkili_rol_id"):
        assert alan in str(h.value)
    kit_ayar.dogrula(dolu_ayar())


def test_kapali_modulun_kimligi_istenmez():
    a = dolu_ayar()
    a["moduller"]["ticket"] = {"acik": False, "kategori_id": 0}
    kit_ayar.dogrula(a)


def test_takma_ad_ve_yas():
    assert takma_ad("{isim} | {yas}", "ahmet   çağrı", "19") == "Ahmet Çağrı | 19"
    assert len(takma_ad("{isim} | {yas}", "a" * 40, "20")) == 32
    assert yas_gecerli("13", 13) and not yas_gecerli("12", 13) and not yas_gecerli("on beş", 13) and not yas_gecerli("150", 13)


def test_spam_sayaci_pencereli():
    s = SpamSayaci(mesaj=3, saniye=5)
    assert [s.ekle(1, t) for t in (0, 1, 2)] == [False] * 3
    assert s.ekle(1, 3) is True          # 5 sn içinde 4. mesaj
    assert [s.ekle(2, t) for t in (0, 6, 12, 18)] == [False] * 4  # yavaş yazan susturulmaz


def test_link_tespiti():
    assert link_var("bak https://x.com/a") and link_var("discord.gg/abc") and link_var("www.site.com")
    assert not link_var("saat 3.30'da buluşalım") and not link_var("")


def test_uyarilar_kalici(tmp_path):
    u = Uyarilar(tmp_path / "u.json")
    assert u.ekle(5, "küfür", "mod") == 1 and u.ekle(5, "spam", "mod") == 2
    assert [x["sebep"] for x in Uyarilar(tmp_path / "u.json").listele(5)] == ["küfür", "spam"]


def test_ticket_yardimcilari():
    assert kanal_adi("Ahmet.Çağrı_99") == "destek-ahmet-a-r-99"
    assert dokum([("2026-10-23 10:00", "Ali", "selam")]) == "[2026-10-23 10:00] Ali: selam"


def test_moduller_bota_yuklenir_komutlar_kayitli():
    import bot as kit_bot

    async def yukle():
        b = kit_bot.Bot(dolu_ayar())
        for yol in kit_bot.MODULLER.values():
            await b.load_extension(yol)
        coglar, komutlar = set(b.cogs), {c.name for c in b.tree.get_commands()}
        await b.close()
        return coglar, komutlar

    coglar, komutlar = asyncio.run(yukle())
    assert coglar == {"Ticket", "Kayit", "Moderasyon"}
    assert {"ticket-panel", "kayit-panel", "ban", "at", "sustur", "temizle", "uyar", "uyarilar"} <= komutlar


def test_paket_ayarsiz_cikmaz_dolu_ayarla_cikar(tmp_path):
    bos = tmp_path / "bos.yaml"
    bos.write_text((KIT / "ayar.ornek.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError):
        paketle(bos, tmp_path)
    dolu = tmp_path / "musteri.yaml"
    dolu.write_text(yaml.safe_dump(dolu_ayar(), allow_unicode=True), encoding="utf-8")
    z = zipfile.ZipFile(paketle(dolu, tmp_path / "cikti"))
    adlar = set(z.namelist())
    assert "discord-bot/ayar.yaml" in adlar and "discord-bot/KURULUM.md" in adlar and "discord-bot/moduller/ticket.py" in adlar
    assert not any(".env" == Path(a).name or "__pycache__" in a for a in adlar)
    assert yaml.safe_load(z.read("discord-bot/ayar.yaml"))["sunucu_id"] == 100


def test_baglanti_yalniz_ipv4(monkeypatch):
    import socket

    import bot as kit_bot
    from discord.ext import commands

    async def bos(self, token):
        return None

    monkeypatch.setattr(commands.Bot, "login", bos)

    async def dene(ayar):
        b = kit_bot.Bot(ayar)
        await b.login("x")
        aile = getattr(b.http.connector, "_family", None)
        await b.close()
        return aile

    assert asyncio.run(dene(dolu_ayar())) == socket.AF_INET
    kapali = {**dolu_ayar(), "yalniz_ipv4": False}
    assert asyncio.run(dene(kapali)) is None
