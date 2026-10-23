---
proje: Tezgah
created: 2026-10-23
type: final-dokuman
status: aktif
---
# Tezgah — Final Doküman

## Özet
Bionluk'ta satılan iki sabit kapsamlı hizmetin teslim kitleri ve satış malzemesi: (1) PDF/taranmış görsel → Excel/Word
dönüştürme, (2) hazır modüllü Discord botu. Kod ve dönüştürme işini Claude yapar, kitler sipariş başı işi dakikalara indirir;
Scryne hesap sahibi olarak yazışır ve teslim eder. Fiverr'da n8n kurulum paketi ilk yorumlardan sonra açılır.

## Kararlar

| # | Karar | Gerekçe |
| --- | --- | --- |
| K-1 | Önce Bionluk, Fiverr koşullu (Bionluk'ta 3 yorum sonrası) | TL ve Türkçe, alıcı isteklerine teklif verilebiliyor; Fiverr ilk sipariş 30–60 gün, Payoneer kesintili (araştırma) |
| K-2 | Dijital PDF → pdfplumber; taranmış → Claude okur + docling ikinci okuma + aritmetik kontrol | S1: pdfplumber %100; tarama Claude %100, NIM %94,6, docling %91,2 (rakam bozabiliyor) |
| K-3 | Bulut görsel modeli yok | Doğruluk düşük, müşteri belgesi üçüncü tarafa gider, NIM ücretsiz katmanı deneme amaçlı |
| K-4 | Uyuşmazlık raporu olmadan tarama teslimi yok | İki bağımsız okumanın uyuşmadığı her hücre ve tutmayan her toplam teslimden önce gösterilir; yanlış rakam teslim edilmez |
| K-5 | Discord bot: Python + discord.py, modüller (ticket, kayıt/doğrulama, moderasyon), müşteriye özel tek `ayar.yaml` | Tek stack; her sipariş ayar değişikliği, yeni kod değil |
| K-6 | Barındırma satılmaz; teslim = paket + Türkçe kurulum rehberi; premium pakette müşterinin sunucusuna bir kerelik kurulum | Bionluk "sınırsız hosting" yasaklı; süregelen barındırma bakım yükü getirir |
| K-7 | Kapsam dışı: ödev/tez, veri çekme botu, toplu veri, gri alan botlar | Bionluk yasaklı hizmetler listesi (destek/72, 2026-10-23 okundu); ödev talebi kibarca reddedilir |
| K-8 | Başlangıç fiyatı düşük, 5 yorumdan sonra artar | Yorumsuz ilan satmıyor (Telegram bot ilanlarının 27/32'si yorumsuz) |

## Teknoloji Stack

| Katman | Seçim | Gerekçe |
| --- | --- | --- |
| Dil, paket | Python 3.12, uv | Makinede kurulu, tek dil |
| CLI | `tezgah` (typer) | `tezgah donustur`, `tezgah bot`, `tezgah defter` |
| PDF metin/tablo | pdfplumber | S1: dijitalde %100, < 0,2 sn |
| Tarama ikinci okuma | docling (+ EasyOCR tr) | Yerel, bedava; Claude'la çapraz kontrol |
| Çıktı | openpyxl, python-docx | Sayılar gerçek sayı, Türkçe biçimle gösterilir |
| Bot | discord.py 2.x | Ticket/kayıt/moderasyon için olgun |
| Test | pytest | Bilinen cevaplı belgeler (S1 seti) regresyon testi olur |

## Mimari
```
sipariş klasörü (calisma/<sipariş-no>/)
  girdi/  → tezgah donustur → dijital mi?  ── evet → pdfplumber → tablo
                                           └─ hayır → Claude okur (oturumda) + docling okur → karşılaştır
          → aritmetik kontrol (satır çarpımı, toplamlar) → uyuşmazlık raporu → Excel/Word
  cikti/  → Scryne teslim eder;  tezgah defter ekle → defter.csv
```
Discord: `kitler/discord-bot/` kaynak + `tezgah bot paketle <ayar.yaml>` → müşteriye zip (kod, ayar, rehber).

## Kapsam (v1)
- Süre: kitler ve ilanlar ~1 hafta; sonra 30 günlük satış penceresi.
- Bitti = kullanıldı: iki ilan Bionluk'ta yayında, en az bir gerçek ücretli sipariş kitle teslim edildi ve alıcı onayladı.
- Öldürme: yayından 30 gün sonra 0 sipariş → fiyat/paket/platform yeniden açılır.

## Riskler ve Doğrulamalar
- S1 (✅ 2026-10-23, `spikes/s1-donusturme/SONUC.md`): motor seçimi. Sınır: sentetik tarama; el yazısı, fotoğraf
  perspektifi, birleşik hücre ölçülmedi → ilk gerçek siparişlerde hata defteri.
- Claude okuması Scryne'ın abonelik limitinden yer: 50+ sayfalık taramada sınır var, büyük paketin sayfa tavanı buna göre.
- Bionluk görünürlük mekaniği açık değil; ilk yorumlar alıcı isteklerine teklifle aranır.

## Kapsam Dışı
- Veri çekme/firma listesi, ödev, barındırma, Armut, Upwork, müşteri yazışmasının otomasyonu, sürekli revizyonlu özel proje.
