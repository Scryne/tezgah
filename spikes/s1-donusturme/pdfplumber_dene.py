import pdfplumber, time
from ortak import puanla
for ad in ["a_fiyat_listesi", "b_fatura", "c_uzun_iki_sayfa"]:
    t = time.time(); rows = []
    with pdfplumber.open(f"veri/{ad}.pdf") as pdf:
        for p in pdf.pages:
            for tb in p.extract_tables(): rows += tb
    i, n, h = puanla(ad, rows)
    print(f"pdfplumber {ad}: {i}/{n} = {i/n:.1%}  {time.time()-t:.1f}s", h[:3])
