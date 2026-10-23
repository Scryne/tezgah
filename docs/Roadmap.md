---
proje: Tezgah
created: 2026-10-23
type: roadmap
status: aktif
---
# Tezgah — Roadmap

Durum sütunu session-start hook'u tarafından otomatik okunur — format bozulmasın:
⏳ Bekliyor / 🔄 Devam Ediyor / ✅ Tamamlandı / ⛔ Engelli.

| Faz | Adı | Durum | Bitti Kriteri |
| --- | --- | --- | --- |
| 0 | Spike S1: dönüştürme motoru | ✅ Tamamlandı | Bilinen cevaplı Türkçe test setinde motorlar ölçüldü, karar K-2 (`spikes/s1-donusturme/SONUC.md`) |
| 1 | İskelet ve sağlık | ✅ Tamamlandı | uv projesi + `tezgah` CLI; CI (lint + test) yeşil; `.github/dependabot.yml`; repo GitHub'da (private, Scryne onayıyla) |
| 2 | Dönüştürme kiti | ✅ Tamamlandı | `tezgah donustur` dijital PDF'i ve taramayı Excel/Word'e çeviriyor; S1 seti regresyon testi %100; bozuk okuma uyuşmazlık raporunda yakalanıyor; örnek çıktılar ilan görseline hazır |
| 3 | Discord bot kiti | ✅ Tamamlandı | Ticket, kayıt, moderasyon modülleri bir test sunucusunda gerçekten çalıştı; `tezgah bot paketle` müşteri zip'ini + Türkçe rehberi üretiyor |
| 4 | Satış malzemesi | ✅ Tamamlandı | İki Bionluk ilanı (3'er paket, kurallara uygun başlık), örnek görseller, sipariş kartı, mesaj şablonları, `tezgah defter` |
| 5 | Yayın (Scryne) | 🔄 Devam Ediyor | Scryne üyeliği açtı, IBAN girdi, iki ilan onaylandı ve yayında |
| 6 | Gerçek kullanım | ⏳ Bekliyor | En az bir gerçek ücretli sipariş kitle teslim edildi, alıcı onayladı; 30 gün sonunda defter üzerinden karar |
| 7 | Fiverr n8n paketi (koşullu) | ⏳ Bekliyor | Bionluk'ta 3 yorum sonrası: n8n kurulum kiti + gig + Payoneer yolu |

## Faz Detayları

### Faz 1: İskelet ve sağlık
- **İşler:** `pyproject.toml` (uv), `src/tezgah/` + typer CLI, pytest, ruff, GitHub Actions, dependabot (uv).
- **Notlar:** private `Scryne/tezgah` (10-24), CI yeşil (`d72ad87`), Dependabot + güvenlik uyarıları açık. gh token'ında workflow kapsamı yok; push git credential manager ile.

### Faz 2: Dönüştürme kiti
- **İşler:** sipariş klasörü düzeni; dijital/tarama ayrımı (metin katmanı var mı); pdfplumber çıkarımı; docling ikinci okuma;
  Claude okumasının girdi biçimi (`okuma_claude.json`); hücre karşılaştırma + aritmetik kontrol; Excel (sayılar sayı) ve Word yazımı;
  proje skill'i `donustur` (Claude'un oturumda izleyeceği adımlar).
- **Durum (10-23):** çekirdek, kontroller, skill ve 24 test bitti; uçtan uca taramada 360/360. Kapak görseli Faz 4'te (`docs/satis/gorseller/kapak-donustur.png`).
- **Öğrenilen:** docling tek başına teslim edilemez ama iyi tanık; asıl güvence satır aritmetiği. Kontrol gürültülü olursa
  her sipariş yorucu olur, bu yüzden hesabı tutan satır güvenli sayıldı.

### Faz 3: Discord bot kiti
- **İşler:** discord.py bot, modül seçimi `ayar.yaml`'dan; slash komutları; paketleme; rehber. Test sunucusu ve bot token'ı Scryne açar
  (Discord geliştirici portalı, bir kerelik).
- **Durum (10-24):** kit (`kitler/discord-bot`, discord.py 2.7.1) + `tezgah bot <ayar.yaml>` paketleme + Türkçe KURULUM.md + 9 test
  (modüller bota yükleniyor, 8 komut kayıtlı, eksik kimlikle paket çıkmıyor). Kalan: gerçek test sunucusunda çalıştırma (token Scryne'da).
- **Gerçek sunucu testi (10-24):** müşteri paketi birebir açılıp kuruldu (`scripts/test_sunucu_kur.py` rol/kanal açar, ayarı yazar);
  Scryne ticket aç/kapat, kayıt formu, /temizle, /uyar'ı denedi, hepsi çalıştı, `#bot-log`'a düştü, bot logunda hata 0.
- **Öğrenilen (üç kusur, düzeltildi):** (1) açılışta gateway 503'te discord.py yeniden bağlanmadan çöküyor → `main` 10 deneme;
  (2) boşta kalan botun ilk isteği AAAA DNS'te 11,6 sn bekleyip 3 sn sınırını kaçırdı ("Uygulama yanıt vermedi") → yalnız IPv4 +
  her etkileşimde önce defer; (3) döküm saatleri UTC'ydi → yerel saat. Kaçırılan: yeni üye girişi (kayıtsız rolü, hoş geldin) ve
  bağlantı engeli sahibin hesabıyla sınanamadı; ilk gerçek siparişte alıcının sunucusunda izlenir.

### Faz 5: Yayın
- **10-24:** üyelik + IBAN tamam; PDF→Excel ilanı Teknolojik Destek'te onaylandı ve yayında (başlık 60 karakter sınırına göre kısaltıldı). Sayaç 10-24. Sırada Discord ilanı.

### Faz 4: Satış malzemesi
- **İşler:** ilan metinleri ("Ben … fiil" başlık, iletişim bilgisi yok), paket fiyatları (K-8), örnek önce/sonra görselleri,
  sipariş kartı (adım adım), mesaj şablonları (karşılama, gereksinim, teslim, yorum isteği, ödev reddi), defter CSV.
- **Durum (10-24):** `docs/satis/` (iki ilan, sipariş kartı, mesajlar, iki kapak 1280×720), `tezgah defter ekle|yayin|ozet`,
  `bot-siparisi` skill'i. Fiyatlar rakip taramasından (2026-10-24): PDF 100/250/500 TL, Discord 250/600/1.200 TL.
- **Not:** Discord kapağı ve ilanı "test edilmiş modüller" diyor; Faz 3'ün gerçek sunucu testi bitmeden ilan yayına girmez.
