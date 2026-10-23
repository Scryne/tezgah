---
proje: Tezgah
created: 2026-10-23
type: proje-fikri
status: taslak
---
# Tezgah — Proje Fikri

## Problem
Scryne'ın otomatik gelir kolları (Matbaa, Otomat, TradeBot, Yanki) kurulu ama bugüne kadar para getirmedi; hepsi bir
algoritmanın göstermesine ya da zamana bağlı. Scryne beklemeden, olasılığa en az bağlı para istiyor. Bunun en yakın yolu
emek karşılığı küçük yazılım işleri (freelance). Scryne daha önce denedi, ilk siparişi alamadı. Araştırmaya göre asıl kilit
yorumsuz ilan: alıcı yorumsuz satıcıdan almıyor (Bionluk'ta Telegram bot ilanlarının 32'sinden 27'si yorumsuz).

Tezgah, siparişten önce kurulmuş **teslim kitleri** ve hazır ilanlardan oluşur. Kod işini Claude yapar. Sipariş başı Scryne'a
kalan iş (talebi okumak, kiti çalıştırmak ya da Claude'a vermek, teslim etmek) 10-15 dakikaya iner.

Araştırma: `docs/arastirma/2026-10-23-freelance.md` (TR: Bionluk canlı sayım; global: Fiverr/Upwork, ödeme yolları).

## Hedef Kullanıcı
- **İşletmeci:** Scryne. Hesap sahibi, müşteriyle yazışan, teslimi yükleyen.
- **Alıcı:** Bionluk'ta küçük işletme, öğrenci, ofis çalışanı (PDF/görsel → Excel); Discord sunucu sahibi (bot);
  Fiverr'da otomasyon isteyen küçük işletme (n8n).

## v1: Kapsam ve "Bitti" Tanımı
- **Süre tavanı:** kitler ve ilanlar ~1 hafta; sonra 30 günlük satış penceresi.
- **Bitti = kullanıldı:** Scryne Bionluk'ta iki ilanı yayına aldı, en az bir gerçek ücretli sipariş kitle teslim edildi ve
  alıcı onayladı (para Bionluk bakiyesine geçti). Testlerin yeşil olması bunun yerine geçmez.
- **Öldürme kriteri:** ilanlar yayına girdikten 30 gün sonra hiç sipariş yoksa yön yeniden açılır (fiyat, paket, platform).
- **Temel özellikler:**
  1. **Dönüştürme kiti:** PDF/taranmış görsel → Excel/Word. Tek komut, tablo yapısı korunur, Türkçe karakter doğru, teslimden
     önce kaynakla karşılaştıran bir doğruluk kontrolü (yanlış rakam teslim edilmez).
  2. **Discord bot kiti:** ticket, kayıt/doğrulama, moderasyon modülleri. Müşteriye özel kısım tek ayar dosyası; teslim paketi
     (kurulum rehberi + barındırma seçenekleri).
  3. **İlanlar:** Bionluk'ta iki ilan (her biri üç paket: temel/standart/premium), kurallara uygun başlık ("Ben … fiil",
     iletişim bilgisi yok), örnek çıktı görselleri.
  4. **Sipariş kartı:** sipariş gelince Scryne'ın sırayla yapacağı adımlar + müşteri mesaj şablonları (selam, gereksinim
     sorusu, teslim, yorum isteği).
  5. **Defter:** sipariş, tutar, süre, yorum kaydı (öldürme kriteri ve fiyat kararı için ölçüm).
  6. **Fiverr n8n paketi (koşullu):** ilk Bionluk yorumları geldikten sonra; self-host kurulum + 1 workflow, Payoneer ödeme yolu.

## Kapsam Dışı
- Kişisel veri/firma listesi çıkarma, Google Maps ve web scraping ilanları: Bionluk'un yasaklı hizmetler listesinde
  ("bot yazılımla veri çekme", toplu veri/e-posta satışı); talep olsa da hesabı riske atar.
- Gri alan istekler (hit/trafik botu, Instagram/SMM botu, SMS onay).
- Armut (teklif başına ücret, iş alınmasa da yanıyor), Upwork (teklif yazışması, Connect maliyeti) — v1'de yok.
- Müşteriyle yazışmanın otomasyonu: platform kuralları ve güven gereği hesap sahibi yazar.
- Sürekli revize isteyen özel projeler: paket kapsamı dışındaki talep ya ek ücretle ya reddedilir.

## Açık Sorular
- Dönüştürme motoru: yerel (docling / PaddleOCR / Tesseract) mı, görme yetenekli bir LLM mi? Türkçe tablolu gerçek PDF'lerle
  spike gerekiyor (doğruluk + maliyet + hız).
- Discord bot dili ve barındırma: discord.py mı discord.js mi; müşteri kendi mi barındırır, yoksa barındırma ek paket mi?
- Bionluk'un yapay zekâ kullanımı kuralı (Fiverr: serbest, sorulursa beyan). Bionluk'ta doğrulanmadı.
- Bionluk üyelik ücreti 149,90 TL (resmî sayfa) — Scryne öder. Para çekmede minimum tutar ve fatura şartı doğrulanmadı.
- İlk yorumlar için başlangıç fiyatı: ne kadar düşük, kaç siparişten sonra yükselir.
