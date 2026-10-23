import time, sys
from pathlib import Path
from docling.document_converter import DocumentConverter, ImageFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions, RapidOcrOptions, TableFormerMode
from ortak import puanla

motor = sys.argv[1] if len(sys.argv) > 1 else "easyocr"
po = PdfPipelineOptions(do_ocr=True, do_table_structure=True, force_full_page_ocr=True)
po.table_structure_options.mode = TableFormerMode.ACCURATE
po.ocr_options = EasyOcrOptions(lang=["tr", "en"], force_full_page_ocr=True) if motor == "easyocr" else RapidOcrOptions(force_full_page_ocr=True)
conv = DocumentConverter(format_options={InputFormat.IMAGE: ImageFormatOption(pipeline_options=po)})
for ad, sayfalar in [("a_fiyat_listesi", 1), ("b_fatura", 1), ("c_uzun_iki_sayfa", 2)]:
    t = time.time(); rows = []
    for s in range(1, sayfalar + 1):
        doc = conv.convert(f"veri/{ad}_tarama_s{s}.jpg").document
        for tb in doc.tables:
            df = tb.export_to_dataframe(doc=doc)
            rows += [list(df.columns)] + df.astype(str).values.tolist()
    i, n, h = puanla(ad, rows)
    print(f"docling-{motor} {ad}: {i}/{n} = {i/n:.1%}  {time.time()-t:.1f}s", h[:4], flush=True)
