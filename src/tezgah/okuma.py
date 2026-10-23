"""Girdi belgelerini okur. Dijital PDF pdfplumber ile; taranmış sayfa görüntüye çevrilir (Claude okur), docling ikinci okumayı yapar."""
import json
import re
import unicodedata
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image

GORSEL = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
DESTEK = GORSEL | {".pdf"}


def temizle(hucre) -> str:
    s = unicodedata.normalize("NFC", str(hucre if hucre is not None else ""))
    return re.sub(r"\s+", " ", s).strip()


def dijital_mi(pdf_yolu: Path, esik: int = 30) -> bool:
    """Metin katmanı olan PDF dijitaldir. İlk üç sayfada hiç ya da çok az karakter varsa taranmıştır."""
    with pdfplumber.open(pdf_yolu) as pdf:
        return sum(len(p.chars) for p in pdf.pages[:3]) >= esik


def pdf_tablolari(pdf_yolu: Path) -> list[dict]:
    tablolar = []
    with pdfplumber.open(pdf_yolu) as pdf:
        for no, sayfa in enumerate(pdf.pages, 1):
            bulunan = sayfa.extract_tables()
            if not bulunan:  # çizgisiz tablo: metin hizasından dene
                bulunan = sayfa.extract_tables({"vertical_strategy": "text", "horizontal_strategy": "text"})
            for t in bulunan:
                satirlar = [[temizle(c) for c in r] for r in t if any(c for c in r)]
                if satirlar:
                    tablolar.append({"kaynak": pdf_yolu.stem, "sayfa": no, "satirlar": satirlar})
    return tablolar


def sayfa_goruntuleri(yol: Path, hedef: Path, dpi: int = 200) -> list[Path]:
    """Taranmış PDF'in ya da görselin sayfalarını Claude'un okuyacağı PNG'lere çevirir."""
    hedef.mkdir(parents=True, exist_ok=True)
    cikti = []
    if yol.suffix.lower() == ".pdf":
        doc = pdfium.PdfDocument(str(yol))
        for i in range(len(doc)):
            p = hedef / f"{yol.stem}_s{i + 1}.png"
            if not p.exists():
                doc[i].render(scale=dpi / 72).to_pil().save(p)
            cikti.append(p)
    else:
        p = hedef / f"{yol.stem}_s1.png"
        if not p.exists():
            Image.open(yol).convert("RGB").save(p)
        cikti.append(p)
    return cikti


def kaynak_ve_sayfa(goruntu: Path) -> tuple[str, int]:
    kok, _, no = goruntu.stem.rpartition("_s")
    return kok, int(no)


def docling_oku(goruntuler: list[Path]) -> list[dict]:
    """Bağımsız ikinci okuma. docling yoksa ImportError yükselir; çağıran karar verir."""
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions, TableFormerMode
    from docling.document_converter import DocumentConverter, ImageFormatOption

    po = PdfPipelineOptions(do_ocr=True, do_table_structure=True, force_full_page_ocr=True)
    po.table_structure_options.mode = TableFormerMode.ACCURATE
    po.ocr_options = EasyOcrOptions(lang=["tr", "en"], force_full_page_ocr=True)
    conv = DocumentConverter(format_options={InputFormat.IMAGE: ImageFormatOption(pipeline_options=po)})
    tablolar = []
    for g in goruntuler:
        kaynak, sayfa = kaynak_ve_sayfa(g)
        doc = conv.convert(str(g)).document
        for tb in doc.tables:
            df = tb.export_to_dataframe(doc=doc)
            satirlar = [[temizle(c) for c in df.columns]] + [[temizle(c) for c in r] for r in df.astype(str).values]
            tablolar.append({"kaynak": kaynak, "sayfa": sayfa, "satirlar": satirlar})
    return tablolar


def json_oku(yol: Path) -> dict:
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}


def json_yaz(yol: Path, veri) -> None:
    yol.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
