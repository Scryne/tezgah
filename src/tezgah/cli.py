"""tezgah komutları."""
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Annotated

import typer

from . import proje_koku
from .bot import paketle
from .defter import OLDURME_GUN, Defter
from .donustur import donustur as _donustur
from .sayi import kucult

_TR_ASCII = str.maketrans("çğıöşü", "cgiosu")

# Windows konsolu cp1254: Türkçe ve ok işaretleri hata vermesin
for _akis in (sys.stdout, sys.stderr):
    if hasattr(_akis, "reconfigure"):
        _akis.reconfigure(encoding="utf-8", errors="replace")

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Tezgah: freelance teslim kitleri")
KOK = proje_koku() / "calisma"


@app.command()
def yeni(ad: Annotated[str, typer.Argument(help="Sipariş adı, ör. bionluk-ahmet-fatura")]):
    """Sipariş klasörü açar: calisma/<tarih>-<ad>/girdi."""
    slug = re.sub(r"[^a-z0-9-]+", "-", kucult(ad).translate(_TR_ASCII)).strip("-")
    klasor = KOK / f"{dt.date.today():%Y-%m-%d}-{slug}"
    (klasor / "girdi").mkdir(parents=True, exist_ok=True)
    typer.echo(f"Müşterinin dosyalarını şuraya koy: {klasor / 'girdi'}")


@app.command()
def donustur(
    klasor: Annotated[Path, typer.Argument(help="Sipariş klasörü")],
    word: Annotated[bool, typer.Option("--word", help="Excel'e ek olarak Word dosyası")] = False,
    ikinci_okuma: Annotated[bool, typer.Option(help="Taramada docling ile bağımsız ikinci okuma")] = True,
):
    """PDF/görsel -> Excel (ve Word). Taranmış sayfalarda Claude okuması + kontrol ister."""
    s = _donustur(klasor, word=word, ikinci_okuma=ikinci_okuma)
    for n in s.notlar:
        typer.echo(f"- {n}")
    if s.durum == "BEKLIYOR":
        typer.echo(f"BEKLIYOR: {len(s.bekleyen)} sayfa Claude okuması bekliyor (okuma_claude.json):")
        for p in s.bekleyen:
            typer.echo(f"  {p}")
        raise typer.Exit(2)
    if s.durum == "INCELE":
        typer.echo(f"INCELE: {len(s.bulgular)} bulgu, ayrıntı {klasor / 'rapor.md'}. Teslim dosyası yazılmadı.")
        raise typer.Exit(1)
    typer.echo("TEMIZ: " + ", ".join(str(p) for p in s.ciktilar))


@app.command()
def bot(
    ayar: Annotated[Path, typer.Argument(help="Müşterinin doldurulmuş ayar.yaml'ı (şablon: kitler/discord-bot/ayar.ornek.yaml)")],
    cikti: Annotated[Path | None, typer.Option(help="Zip'in yazılacağı klasör (varsayılan: ayarın klasörü)")] = None,
):
    """Discord bot kitini müşteriye özel ayarla zip'ler."""
    try:
        zip_yolu = paketle(ayar, cikti or ayar.parent)
    except ValueError as e:
        typer.echo(str(e))
        raise typer.Exit(1) from None
    typer.echo(f"Paket hazır: {zip_yolu}")


defter_app = typer.Typer(no_args_is_help=True, help="Sipariş defteri (veri/defter.csv)")
app.add_typer(defter_app, name="defter")
DEFTER = proje_koku() / "veri"


@defter_app.command("ekle")
def defter_ekle(
    hizmet: Annotated[str, typer.Argument(help="donustur | discord")],
    tutar: Annotated[float, typer.Argument(help="Alıcının ödediği TL")],
    paket: Annotated[str, typer.Option(help="temel | standart | premium")] = "",
    not_: Annotated[str, typer.Option("--not", help="Sipariş no, süre, sorun")] = "",
):
    """Teslim edilen siparişi deftere yazar (net = %20 komisyon düşülmüş)."""
    s = Defter(DEFTER).ekle(hizmet, tutar, paket, not_)
    typer.echo(f"Yazıldı: {s['tarih']} {hizmet} {s['tutar_tl']} TL (net {s['net_tl']})")


@defter_app.command("yayin")
def defter_yayin(tarih: Annotated[str, typer.Argument(help="İlanların yayına girdiği gün, YYYY-AA-GG")]):
    """Öldürme kriterinin sayacını başlatır."""
    Defter(DEFTER).yayin_ayarla(dt.date.fromisoformat(tarih))
    typer.echo(f"Yayın tarihi {tarih}; {OLDURME_GUN} günde sipariş yoksa yön yeniden açılır.")


@defter_app.command("ozet")
def defter_ozet():
    """Sipariş sayısı, brüt/net gelir, yayından beri gün ve öldürme kriteri."""
    o = Defter(DEFTER).ozet()
    typer.echo(f"Sipariş: {o.siparis} · brüt {o.brut:,.2f} TL · net {o.net:,.2f} TL")
    typer.echo(f"Yayın: {o.yayin or 'girilmedi'}" + (f" · {o.gun}. gün" if o.gun is not None else ""))
    if o.oldurme:
        typer.echo(f"ÖLDÜRME KRİTERİ: {OLDURME_GUN} günde sipariş yok, fiyat/paket/platform yeniden açılır.")


bionluk_app = typer.Typer(no_args_is_help=True, help="Bionluk panelini salt-okunur okur")
app.add_typer(bionluk_app, name="bionluk")


@bionluk_app.command("giris")
def bionluk_giris():
    """Ayrı tarayıcı profilinde Bionluk giriş sayfasını açar; giriş yapıp pencereyi kapat."""
    from . import bionluk

    typer.echo("Açılan pencerede Bionluk'a giriş yap, sonra pencereyi kapat.")
    bionluk.giris()
    typer.echo("Oturum kaydedildi.")


@bionluk_app.command("istekler")
def bionluk_istekler():
    """Bana Uygun Alıcı İstekleri sayfasını okuyup calisma/istekler/ altına yazar."""
    from . import bionluk

    try:
        typer.echo(f"Kaydedildi: {bionluk.istekler()}")
    except PermissionError as e:
        typer.echo(str(e))
        raise typer.Exit(1) from None
