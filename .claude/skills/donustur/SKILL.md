---
name: donustur
description: Tezgah dönüştürme siparişini uçtan uca işler — müşterinin PDF/taranmış görselini Excel (ve Word) dosyasına çevirir, taranmış sayfaları Claude okur, docling ikinci okuma + aritmetik kontrolle yanlış rakam teslim edilmez. "dönüştür", "PDF'i Excel'e çevir", "sipariş geldi", "bu dosyayı Excel yap" dendiğinde ya da calisma/ altında yeni bir sipariş klasörü varken kullan.
---

# Dönüştürme siparişi

Amaç: müşteriye yanlış rakam gitmesin. Bir hücreyi "doğru" saymanın tek yolu görüntüye bakmaktır.

## Adımlar

1. **Klasör.** `uv run tezgah yeni <siparis-adi>` → çıkan `calisma/<tarih>-<ad>/girdi/` içine müşterinin dosyaları.
   Scryne dosyayı başka yere indirdiyse oradan kopyala. Müşteri belgesi repoya girmez (`calisma/` gitignore'da).
2. **İlk koşu.** `uv run tezgah donustur calisma/<klasor> [--word]`
   - Dijital PDF'ler doğrudan okunur. Hepsi dijitalse ve hesap tutuyorsa sonuç TEMIZ, 5. adıma geç.
   - Taranmış sayfa varsa sayfa görüntüleri `sayfalar/` altına yazılır, docling ikinci okumayı yapar (sayfa başına ~1 dk), çıkış `BEKLIYOR`.
3. **Claude okuması.** Listelenen her PNG'yi Read ile aç ve `calisma/<klasor>/okuma_claude.json` yaz:
   ```json
   {"tablolar": [{"kaynak": "<dosya adı, uzantısız, _sN yok>", "sayfa": 1,
                  "satirlar": [["Başlık 1", "Başlık 2"], ["hücre", "1.234,56"]]}]}
   ```
   - Başlık satırı dahil. Hücreyi gördüğün gibi yaz: Türkçe harf, sembol (Ø), sayı biçimi (`1.234,56`) değişmez.
   - Boş hücre `""`. Okuyamadığın hücre `"??"` (kontrol bunu yakalar; tahmin etme).
   - Sayfada tablo yoksa `"satirlar": []`. Tablo dışı başlık bilgisi (fatura no, tarih) müşteri istediyse ayrı tablo olarak eklenir.
   - Yazı küçükse sayfayı parçalara kırp (PIL) ve parçaları oku; tek bakışta okunmayan hücreyi uydurma.
4. **Kontrol.** Komutu yeniden çalıştır. `INCELE` ise `rapor.md`'deki her bulgu için görüntüye bak:
   - Okuman yanlışsa `okuma_claude.json`'u düzelt.
   - Belgede gerçekten öyle yazıyorsa (müşterinin belgesindeki hesap hatası dahil) `"dogrulandi": [{"kaynak", "sayfa", "satir", "sutun"}]`
     listesine ekle. Belgedeki hesap hatasını Scryne'a ayrıca söyle, müşteriye iletilecek bir not olur.
   - `okuma_docling.json`'u kontrolü geçirmek için asla düzenleme; o bağımsız tanık.
5. **Teslim.** `TEMIZ` → `cikti/` altındaki dosyayı aç (openpyxl ile satır sayısı + ilk/son satır), sayfadaki satır sayısıyla tut.
   Scryne'a teslim dosyasının tam yolunu ve gerekiyorsa müşteriye not (belgedeki hata, okunamayan yer) ver.

## Sınırlar
- El yazısı, gölgeli fotoğraf, birleşik hücreli karmaşık tablo S1'de ölçülmedi: bunlarda her hücreyi iki kez oku, şüpheli kalanı `??` bırak ve Scryne'a söyle.
- Çok sayfalı tarama Scryne'ın abonelik limitinden yer; 50 sayfa üstü sipariş kabul edilmeden önce sayfa sayısı sorulur.
