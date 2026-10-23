"""Sipariş klasörünü baştan sona işler. Durumlar:
BEKLIYOR: taranmış sayfalar var, Claude okuması (okuma_claude.json) yok ya da eksik.
INCELE:   okumalar arasında uyuşmazlık ya da tutmayan hesap var; teslim dosyası yazılmaz.
TEMIZ:    teslim dosyaları cikti/ altında."""
from dataclasses import dataclass, field
from pathlib import Path

from . import kontrol, okuma, yaz

CLAUDE = "okuma_claude.json"
DOCLING = "okuma_docling.json"
RAPOR = "rapor.md"


@dataclass
class Sonuc:
    durum: str
    bekleyen: list[Path] = field(default_factory=list)
    bulgular: list[kontrol.Bulgu] = field(default_factory=list)
    ciktilar: list[Path] = field(default_factory=list)
    notlar: list[str] = field(default_factory=list)


def donustur(klasor: Path, word: bool = False, ikinci_okuma: bool = True) -> Sonuc:
    girdiler = sorted(p for p in (klasor / "girdi").iterdir() if p.suffix.lower() in okuma.DESTEK)
    if not girdiler:
        raise FileNotFoundError(f"{klasor / 'girdi'} içinde desteklenen dosya yok ({', '.join(sorted(okuma.DESTEK))})")

    notlar, tablolar, goruntuler = [], [], []
    for g in girdiler:
        if g.suffix.lower() == ".pdf" and okuma.dijital_mi(g):
            bulunan = okuma.pdf_tablolari(g)
            tablolar += bulunan
            notlar.append(f"{g.name}: dijital PDF, {len(bulunan)} tablo")
        else:
            sayfalar = okuma.sayfa_goruntuleri(g, klasor / "sayfalar")
            goruntuler += sayfalar
            notlar.append(f"{g.name}: taranmış, {len(sayfalar)} sayfa görüntüsü")

    claude = okuma.json_oku(klasor / CLAUDE)
    bulgular: list[kontrol.Bulgu] = []
    if goruntuler:
        okunan = {(t["kaynak"], t["sayfa"]) for t in claude.get("tablolar", [])}
        bekleyen = [g for g in goruntuler if okuma.kaynak_ve_sayfa(g) not in okunan]
        if ikinci_okuma and not (klasor / DOCLING).exists():
            try:
                okuma.json_yaz(klasor / DOCLING, {"tablolar": okuma.docling_oku(goruntuler)})
            except ImportError:
                notlar.append("docling kurulu değil: ikinci okuma yok (uv sync --extra tarama)")
        if bekleyen:
            return Sonuc("BEKLIYOR", bekleyen=bekleyen, notlar=notlar)
        ikinci = okuma.json_oku(klasor / DOCLING).get("tablolar")
        if ikinci is not None:
            bulgular += kontrol.karsilastir(claude["tablolar"], ikinci)
        else:
            notlar.append("ikinci okuma yok: uyuşmazlık kontrolü yapılmadı, yalnız aritmetik")
        tablolar += [t for t in claude["tablolar"] if t["satirlar"]]

    for t in tablolar:
        bulgular += kontrol.aritmetik(t) + kontrol.bicim(t)
    bulgular = kontrol.suz(bulgular, claude.get("dogrulandi", []))
    rapor_yaz(klasor / RAPOR, notlar, bulgular)
    if bulgular:
        return Sonuc("INCELE", bulgular=bulgular, notlar=notlar)

    cikti = klasor / "cikti"
    cikti.mkdir(exist_ok=True)
    birlesik = yaz.birlestir(tablolar)
    ciktilar = [cikti / f"{klasor.name}.xlsx"]
    yaz.excel_yaz(birlesik, ciktilar[0])
    if word:
        ciktilar.append(cikti / f"{klasor.name}.docx")
        yaz.word_yaz(birlesik, ciktilar[1])
    return Sonuc("TEMIZ", ciktilar=ciktilar, notlar=notlar)


def rapor_yaz(yol: Path, notlar: list[str], bulgular: list[kontrol.Bulgu]) -> None:
    satirlar = ["# Dönüştürme raporu", "", *[f"- {n}" for n in notlar], ""]
    if not bulgular:
        satirlar.append("**TEMİZ**: uyuşmazlık ve tutmayan hesap yok.")
    else:
        satirlar += [
            f"**İNCELE: {len(bulgular)} bulgu.** Her biri için sayfa görüntüsüne bak: okuma yanlışsa `okuma_claude.json`'u düzelt,",
            "belgede gerçekten böyle yazıyorsa `dogrulandi` listesine ekle. Sonra `tezgah donustur` yeniden.",
            "",
            "| Tür | Kaynak | Sayfa | Satır | Sütun | Değer | Açıklama |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        satirlar += [f"| {b.tur} | {b.kaynak} | {b.sayfa} | {b.satir} | {b.sutun} | {b.deger} | {b.aciklama} |" for b in bulgular]
    yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
