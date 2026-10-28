---
name: trendyol-siparisi
description: Bionluk Trendyol ürün listeleme siparişini ya da ücretsiz deneme isteğini teslim eder — müşterinin Excel'i ya da ürün bağlantısından başlık, açıklama ve özellik düzenlemesi, kurallı kontrol, teslim dosyası. "trendyol siparişi", "ücretsiz deneme istedi", "ürünlerini düzenle" dendiğinde kullan.
---

# Trendyol siparişi

İlan: `docs/satis/ilan-trendyol.md`. Söz: 1 ürün ücretsiz deneme, bilinmeyen bilgi uydurulmaz, panel şifresi istenmez.

1. **Klasör:** `uv run tezgah yeni bionluk-<alici>-trendyol`; müşterinin Excel'i `girdi/` altına (Scryne indirir).
   Ücretsiz denemede Excel yok: ürün sayfasını tarayıcı eklentisiyle oku (başsız tarayıcı Cloudflare'e takılır), sayfadaki
   başlık/özellik/açıklamayı `urunler.json`'a yaz: `[{"barkod": "<ürün no ya da p-… kimliği>", "alanlar": {...}}]`.
2. **Aç:** `uv run tezgah trendyol ac <klasor>` → `duzenleme_claude.json` şablonu.
3. **Düzenle (Claude):** her ürün için
   - başlık 15–100 karakter, ürün tipi + öne çıkan özellik + aranan kelime, büyük harf yok, marka tekrarı yok
   - açıklama ≥150 karakter: malzeme, ölçü, kullanım, bakım, paket; yalnız bilinen bilgiyle
   - özellik: `{"deger": ..., "kaynak": "urun" | "satici" | "gorsel"}`. `urun` = değer mevcut veride geçiyor;
     `satici` = `satici.json`'da aynı değer; `gorsel` = yalnız renk/desen gibi görselden okunan alanlar
   - bilinmeyen her şey `sorular`a; satıcı cevaplayınca `satici.json`'a `{"<barkod>": {"<alan>": "<değer>"}}`
4. **Teslim:** `uv run tezgah trendyol teslim <klasor>`.
   - BEKLIYOR (2): çıkan soru mesajını Scryne'a kopyala-yapıştır olarak ver.
   - INCELE (1): bulguları düzelt, kuralı gevşetme.
   - TEMIZ: `teslim/urunler.md` (+ Excel varsa `teslim/<ad>-duzenlendi.xlsx`, değişen hücreler boyalı, Değişiklikler sayfası).
5. **Scryne'a:** teslim mesajı + dosya yolları; sipariş onaylanınca `uv run tezgah defter ekle trendyol <tutar> --paket <ad>`.
