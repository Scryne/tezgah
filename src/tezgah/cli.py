"""tezgah komutları."""
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Annotated

import typer

from .donustur import donustur as _donustur
from .sayi import kucult

_TR_ASCII = str.maketrans("çğıöşü", "cgiosu")

# Windows konsolu cp1254: Türkçe ve ok işaretleri hata vermesin
for _akis in (sys.stdout, sys.stderr):
    if hasattr(_akis, "reconfigure"):
        _akis.reconfigure(encoding="utf-8", errors="replace")

app = typer.Typer(no_args_is_help=True, add_completion=False, help="Tezgah: freelance teslim kitleri")
KOK = Path.cwd() / "calisma"


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
