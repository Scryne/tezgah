"""S1 test seti: cevabı bilinen Türkçe tablolu belgeler (dijital PDF + taranmış görünümlü PNG)."""
import json, random
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialB", "C:/Windows/Fonts/arialbd.ttf"))
OUT = Path("veri"); OUT.mkdir(exist_ok=True)
rnd = random.Random(7)

def tl(x):  # 1234.5 -> "1.234,50"
    s = f"{x:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

URUNLER = ["Çelik vida M6", "Şerit metre 5 m", "Kağıt havlu (12'li)", "Işıklı uyarı levhası", "Gönye 30 cm",
           "Döküm boru Ø110", "İş eldiveni (nitril)", "Yağ çözücü sprey", "Göz koruyucu gözlük", "Üçgen reflektör",
           "Ağır hizmet kablo bağı", "Sıcak silikon çubuğu", "Çekiç 500 g", "Öğütücü disk 115 mm", "Şarjlı matkap ucu seti",
           "Pürüzsüz zımpara P120", "Kılavuz çekme takımı", "Çift taraflı bant", "Ölçüm kumpası", "Söküm levyesi",
           "Ğ testi numune kabı", "Isıya dayanıklı önlük", "Özel cıvata M10", "Şeffaf koli bandı", "Kürek (çelik sap)"]
BIRIM = ["adet", "kutu", "paket", "metre", "takım"]

def satirlar(n):
    rows = []
    for i in range(n):
        m = rnd.randint(1, 250); f = round(rnd.uniform(3, 4800), 2)
        rows.append([f"UR-{1000+i*7}", URUNLER[i % len(URUNLER)], rnd.choice(BIRIM), str(m), tl(f), tl(m * f)])
    return rows

def pdf(ad, baslik, ust, basliklar, rows, alt=None):
    st = getSampleStyleSheet(); st["Normal"].fontName = "Arial"; st["Title"].fontName = "ArialB"
    el = [Paragraph(baslik, st["Title"])] + [Paragraph(u, st["Normal"]) for u in ust] + [Spacer(1, 10)]
    t = Table([basliklar] + rows + (alt or []), repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Arial", 8.5), ("FONT", (0, 0), (-1, 0), "ArialB", 8.5),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                           ("ALIGN", (3, 1), (-1, -1), "RIGHT")]))
    el.append(t)
    SimpleDocTemplate(str(OUT / f"{ad}.pdf"), pagesize=A4).build(el)
    (OUT / f"{ad}.json").write_text(json.dumps({"basliklar": basliklar, "satirlar": rows + (alt or [])}, ensure_ascii=False, indent=1), encoding="utf-8")

H = ["Ürün Kodu", "Ürün Adı", "Birim", "Miktar", "Birim Fiyat (TL)", "Tutar (TL)"]
r = satirlar(25); pdf("a_fiyat_listesi", "Fiyat Listesi — Ekim 2026", ["Tedarikçi: Güneş Hırdavat Ltd. Şti."], H, r)
r = satirlar(12); top = sum(float(x[5].replace(".", "").replace(",", ".")) for x in r)
alt = [["", "", "", "", "Ara Toplam", tl(top)], ["", "", "", "", "KDV %20", tl(top * 0.2)], ["", "", "", "", "Genel Toplam", tl(top * 1.2)]]
pdf("b_fatura", "SATIŞ FATURASI", ["Fatura No: GHS2026000418   Tarih: 14.10.2026", "Alıcı: Özdemir İnşaat Taahhüt A.Ş., Çiğli / İzmir"], H, r, alt)
r = satirlar(60); pdf("c_uzun_iki_sayfa", "Depo Sayım Tutanağı", ["Sayım yeri: Manisa OSB 3. Kısım Depo"], H, r)

# taranmış görünüm: 150 dpi, hafif eğim, gürültü, JPEG kalitesi düşük
import pypdfium2 as pdfium
from PIL import Image, ImageFilter
import numpy as np
for p in sorted(OUT.glob("*.pdf")):
    doc = pdfium.PdfDocument(str(p))
    for i in range(len(doc)):
        im = doc[i].render(scale=150 / 72).to_pil().convert("L")
        im = im.rotate(rnd.uniform(-1.2, 1.2), expand=True, fillcolor=255, resample=Image.BICUBIC)
        a = np.asarray(im).astype(np.int16) + np.random.default_rng(i).normal(0, 12, im.size[::-1]).astype(np.int16)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
        im.save(OUT / f"{p.stem}_tarama_s{i+1}.jpg", quality=55)
print(sorted(x.name for x in OUT.iterdir()))
