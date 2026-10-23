# S1 — Dönüştürme motoru (2026-10-23)

**Soru:** PDF/taranmış görsel → Excel işinde hangi motor teslim edilebilir doğrulukta?

**Test seti** (`uret.py`, cevabı bilinen): üç Türkçe tablolu belge (fiyat listesi 25 satır, fatura 12 satır + toplamlar,
iki sayfalık sayım 60 satır); ç ğ ı İ ö ş ü, Ø, `1.234,56` biçimi. Her biri dijital PDF + taranmış görünümlü JPEG
(150 dpi, ±1,2° eğim, gürültü, bulanıklık, JPEG kalite 55). Ölçüm `ortak.py`: ürün koduyla satır eşleştirip hücre hücre birebir.

| Motor | Girdi | Doğruluk (hücre) | Süre | Hata tipi |
|---|---|---|---|---|
| pdfplumber | dijital PDF | 588/588 = %100 | < 0,2 sn | — |
| docling + EasyOCR (yerel, CPU) | tarama | 536/588 = %91,2 | 21–92 sn/belge | Türkçe harf düşüyor (Serit, Gonye), Ø→0, **191,08→191.08 (rakam değişti)**, kelime sırası kayması |
| NVIDIA nemotron-3.5-super-vl-120b | tarama | 556/588 = %94,6 | 42–119 sn/belge | isimlerde uydurma (Gönve, sprej, "İplikli"); rakamlar doğru |
| Claude (Claude Code oturumunda okuma) | tarama | 228/228 = %100 (a + b) | oturum içi | — |

`meta/llama-3.2-90b-vision`: üç belgede de 300 sn'de yanıt yok (zaman aşımı).

**Karar önerisi:**
- Dijital PDF → pdfplumber (deterministik, bedava, anında).
- Taranmış/görsel → Claude okur (Scryne'ın aboneliği, ek maliyet yok), docling bağımsız ikinci okuma olarak çalışır;
  iki okumanın uyuşmadığı hücreler + aritmetik kontrol (miktar × birim fiyat = tutar, ara toplam, KDV) teslimden önce listelenir.
- Bulut modeli (NIM) yok: hem doğruluğu düşük hem müşteri belgesini üçüncü tarafa gönderir, hem de ücretsiz katman deneme içindir.

**Sınır:** sentetik tarama gerçek telefon fotoğrafından temiz. El yazısı, gölge, perspektif ve birleşik hücreli karmaşık
tablolar ölçülmedi; ilk gerçek siparişler bu sınamanın yerine geçer (defterde hata kaydı tutulur).

## Uçtan uca (aynı gün, `tezgah donustur`)
İki sayfalık taranmış PDF (c, 60 satır): docling ikinci okuma + Claude okuması. İlk kontrol 19 bulgu verdi, **19'u da docling'in**
(kaçan tutar hücresi, kelime sırası, M1O, Blrim). Claude okumasında hesap 60/60 satırda tuttu. Bu yüzden: hesabı tutan satırın sayıları
uyuşmazlık sayılmaz, metin OCR gürültüsü tolere edilir ama metindeki rakamlar birebir (K-4 inceltildi). Sonra TEMIZ;
Excel bilinen cevapla 360/360 hücre, iki sayfa tek tabloda, sayılar gerçek sayı. Beş kod bozması (mutasyon) testlerle yakalandı.
