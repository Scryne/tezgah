# Tezgah

Freelance siparişleri için önceden kurulmuş teslim kitleri. Siparişi Scryne alır ve teslim eder, kitler işi
dakikalara indirir. Hedef sipariş başına 10–15 dakika insan işi.

| Kit | Ne yapar | Komut |
|---|---|---|
| Dönüştürme | PDF/görsel → Excel (ve Word). Dijital PDF'i doğrudan okur. Taranmış sayfayı Claude okur, docling bağımsız ikinci okuma yapar, satır aritmetiği ve biçim kontrolü teslimi denetler | `tezgah donustur` |
| Discord bot | Ticket, kayıt, moderasyon modüllü bot. Müşterinin `ayar.yaml`'ıyla zip'lenir | `tezgah bot` |
| Defter | Teslim edilen sipariş, brüt/net gelir, yayından beri gün ve öldürme kriteri (30 gün, 0 sipariş) | `tezgah defter` |
| Bionluk okuyucu | "Bana uygun alıcı istekleri" sayfasını salt-okunur çeker. Teklif vermez, mesaj atmaz | `tezgah bionluk` |

## Kurulum

```bash
uv sync --group dev              # çekirdek + test araçları
uv sync --extra tarama           # taramada ikinci okuma (docling + easyocr, torch indirir)
uv sync --extra bionluk          # Bionluk okuyucu (makinedeki Playwright Chromium kullanılır)
uv run pytest -q && uv run ruff check .
```

## Sipariş akışı

```bash
uv run tezgah yeni bionluk-fatura            # calisma/<tarih>-bionluk-fatura/girdi/ açılır
uv run tezgah donustur calisma/<klasor> --word
#   BEKLIYOR → taranmış sayfalar Claude okuması bekliyor (okuma_claude.json)
#   INCELE   → rapor.md'deki bulgular doğrulanmadan teslim dosyası yazılmaz
#   TEMIZ    → cikti/ altında Excel (ve Word)
uv run tezgah bot calisma/<klasor>/ayar.yaml  # Discord kiti: müşteriye özel zip
uv run tezgah defter ekle donustur 750 --paket standart
uv run tezgah defter ozet
```

Adım adım tarifler `.claude/skills/` altında: `donustur`, `bot-siparisi`, `istek-tara`.

## Düzen

- `src/tezgah/`: komutlar ve kontrol mantığı. `calisma/` ve `veri/` her zaman deponun kökünde açılır; komut başka bir
  klasörden çalışsa da değişmez (`TEZGAH_KOK` ile ezilebilir).
- `kitler/discord-bot/`: müşteriye giden bot kiti (`KURULUM.md` müşteri içindir).
- `docs/satis/`: ilan metinleri, hazır mesajlar, sipariş kartı, ilan görselleri (`gorseller/uret.py`).
- `docs/`: proje fikri, final doküman, roadmap. `spikes/s1-donusturme/`: okuma yöntemlerinin ölçümü (K-2'nin kanıtı).
- `calisma/`: müşteri dosyaları ve Bionluk oturumu. Git'e girmez.
