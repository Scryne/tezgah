---
name: istek-tara
description: Bionluk "Bana Uygun Alıcı İstekleri"ni okur, yeni istekleri Tezgah'ın kapsamına göre süzer ve uygun olanlara 600 karakterlik teklif metni yazar; göndermez. "istekleri tara", "alıcı istekleri", "yeni iş var mı", "teklif bak" dendiğinde kullan.
---

# Alıcı isteklerini tara

1. **Oku:** `uv run tezgah bionluk istekler` → `calisma/istekler/<tarih>.txt`. "oturum yok" derse Scryne'a
   `uv run tezgah bionluk giris` (Google düğmesi değil, e-posta + şifre; Google otomasyon tarayıcısını reddediyor).
   Günde en çok birkaç okuma; panel yalnız okunur, hiçbir düğmeye basılmaz.
2. **Yeni olanı ayır:** bir önceki dosyayla başlıkları karşılaştır. "Teklifimi Göster" görünen istek zaten teklif verilmiş.
3. **Süz (K-7, K-9):**
   - Al: yazılım otomasyonu, yapay zekâ entegrasyonu, PDF/Excel dönüştürme, Discord/Telegram botu, API bağlantısı, içerik hattı.
   - Alma: ödev/tez, öğrenci yarışma projesi (Teknofest, TÜBİTAK yarışması), donanım/elektronik/PCB, yerinde kurulum,
     sürekli saatlik destek, oyun modu, veri çekme botu, takipçi/beğeni, kapsamı belirsiz tek satırlık istekler.
   - Değerlendir: bütçe, yaş (7 günden eski ve 50+ teklif → şans düşük ama bedava), teklif sayısı.
4. **Teklif yaz:** ÖZEL SİPARİŞ; en yakın ilan (otomasyon işleri → "Python ve yapay zekâ ile işlerinizi otomatikleştirebilirim";
   PDF → dönüştürme ilanı; Discord → bot ilanı). Mesaj ≤600 karakter (Python ile ölç), Fiverr dışı iletişim bilgisi yok.
   Fiyat bütçenin içinde; süre gün. Dürüstlük: yapamayacağın şeyi vaat etme; bilinen platform tuzağını (ör. YouTube API audit) söyle.
5. **Sun:** Scryne'a tablo (istek, bütçe/teklif sayısı, karar, neden) + uygunlar için kopyala-yapıştır alanlar
   (ilan, mesaj, ücret, süre). Gönderim Scryne'da.
6. **Kaydet:** gönderilen teklifi `docs/Roadmap.md` Faz 6/8 notuna bir satır olarak ekle.
