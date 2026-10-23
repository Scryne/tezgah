---
name: bot-siparisi
description: Tezgah Discord bot siparişini işler — alıcının kanal/rol kimliklerinden ayar.yaml'ı doldurur, `tezgah bot` ile müşteri zip'ini üretir, premium özelleştirmeyi yapar. "bot siparişi", "discord siparişi", "kimlikler şunlar" dendiğinde kullan.
---

# Discord bot siparişi

1. **Klasör:** `uv run tezgah yeni <siparis-adi>`. Ayar `calisma/<klasor>/ayar.yaml` olur (müşteri verisi repoya girmez).
2. **Ayar:** `kitler/discord-bot/ayar.ornek.yaml`'ı kopyala. Scryne'ın yapıştırdığı kimlikleri doğru alanlara yaz:
   - Satın alınmayan modülde `acik: false`. Temel paket = tek modül.
   - Kimlik 17–20 haneli sayı olmalı; tırnak koyma. Eksik ya da şüpheli kimlik varsa tahmin etme, Scryne'a alıcıya sorulacak cümleyi ver.
   - Premium: alıcının istediği panel/karşılama metinleri ayara; "küçük ek komut" ilgili modüle eklenir, testle birlikte
     (kitin kendisine değil, siparişe özel kopyaya: `calisma/<klasor>/kit/`, paketleme bu kopyadan yapılır).
3. **Paket:** `uv run tezgah bot calisma/<klasor>/ayar.yaml` → eksik alan varsa hangisi olduğunu söyler; yoksa zip'in yolunu verir.
4. **Teslim:** Scryne'a zip yolunu ve `docs/satis/mesajlar.md` / Teslim — Discord metnini ver.
5. **Kurulum yardımı:** alıcının hata ekran görüntüsünde sık sebepler: Members/Message Content intent kapalı, bot rolü verilen
   rolün altında, `applications.commands` olmadan eklenmiş, token `.env`'de değil. KURULUM.md "Sorun giderme" bölümü.
6. **Defter:** `uv run tezgah defter ekle discord <tutar> --paket <paket>`.

Kapsam dışı: müzik botu, oyun sunucusu istatistiği, veri çekme, barındırma (K-6, K-7). İstenirse Scryne'a kapsam dışı mesajını öner.
