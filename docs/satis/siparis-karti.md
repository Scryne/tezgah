# Sipariş kartı

Sipariş bildirimi geldiğinde sırayla. Mesaj metinleri `mesajlar.md`'de. Claude Code'u `Projeler\Tezgah` klasöründe aç;
her adımda ne diyeceğin aşağıda yazıyor.

## Ortak
1. Bionluk'ta siparişi aç, alıcının yazdığını oku.
2. **Ödev mi?** (okul ödevi, "proje ödevim", tez) → `mesajlar.md` / Ödev reddi. Bionluk'ta yasak, alma.
3. **Kapsam dışı mı?** (veri çekme botu, müzik botu, takipçi/beğeni) → kibarca reddet ya da iptal öner.
4. Karşılama mesajını gönder (gerekenleri iste).

## PDF → Excel
5. Dosyaları indir. Claude'a: **"sipariş geldi: <dosyaların yolu>, dönüştür"**.
6. Claude dosyayı okur, kontrol eder ve teslim dosyasının yolunu verir. Bir not verdiyse (belgede hesap hatası, okunamayan yer) teslim mesajına ekle.
7. Dosyayı Bionluk'ta **Teslim Et** ile yükle, teslim mesajını gönder.
8. Claude'a: **"deftere yaz: dönüştürme, <tutar>"**.

## Discord botu
5. Kimlik mesajını gönder. Kimlikler gelince Claude'a yapıştır: **"bot siparişi: <modüller>, kimlikler şunlar: …"**.
6. Claude ayarı doldurur, paketi üretir ve zip'in yolunu verir.
7. Zip'i teslim et, teslim mesajını gönder. Premium'da canlı yardım: alıcı hata alırsa ekran görüntüsünü Claude'a ver.
8. Claude'a: **"deftere yaz: discord, <tutar>"**.

## Teslimden sonra
- Alıcı 3 gün içinde onaylamazsa sipariş otomatik onaylanır.
- Onaydan sonra yorum isteği mesajı (bir kez, ısrar yok).

## Alıcı isteğine teklif (Bana Uygun Alıcı İstekleri)
- Teklif Ver → **ÖZEL SİPARİŞ** (min 100 TL; 100 TL ve üstünde alıcı yorum ve puan verebilir).
- Teklif bir ilana bağlanmak zorunda: isteğin kategorisine en yakın ilanı seç (Diğer Yazılım Teknoloji → Discord ilanı).
- Mesaj en fazla **600 karakter**; süre gün olarak. Uzun açıklama kabul sonrası mesajlaşmaya kalır.
- Teklif verme: ödev, öğrenci yarışma projesi (Teknofest vb.), donanım/elektronik, sürekli saatlik destek.
- Ekran görüntüsünü Claude'a at, isteği değerlendirip metni yazar.
