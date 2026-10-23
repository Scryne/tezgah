# Mesaj şablonları

Kısa ve sade. Bionluk dışı iletişim bilgisi (telefon, e-posta, Discord kullanıcı adı) **yazma**: kural ihlali.

## Karşılama — PDF
```
Merhaba, siparişiniz için teşekkürler. Dönüştürülecek dosyaları buraya ekleyebilir misiniz? Tablonun dışındaki bilgilerin (başlık, tarih, firma adı) Excel'de olmasını isterseniz belirtin. Dosyalar gelince hemen başlıyorum.
```

## Karşılama — Discord
```
Merhaba, siparişiniz için teşekkürler. Botu sunucunuza göre ayarlamam için birkaç kimlik gerekiyor:

1. Discord > Kullanıcı Ayarları > Gelişmiş > Geliştirici Modu'nu açın.
2. Aşağıdakilerin üzerine sağ tıklayıp "ID'yi Kopyala" deyin ve buraya yapıştırın:
- Sunucu (sunucu adına sağ tık)
- Bot kayıtlarının düşeceği kanal
- Ticket için: destek kanallarının açılacağı kategori, destek ekibi rolü
- Kayıt için: kayıtsız rolü, üye rolü, hoş geldin kanalı
- Moderasyon için: moderatör rolü

Rol yoksa önce oluşturmanız yeterli.
```

## Teslim — PDF
```
Dosyanız hazır, ekte. Rakamlar Excel'de sayı olarak duruyor, toplam ve formül kullanabilirsiniz. Tablonun hesabını (satır tutarları ve toplamlar) kontrol ettim. Bir şey eksik ya da farklı olsun isterseniz yazmanız yeterli.
```
Belgede hesap hatası bulunduysa ekle:
```
Not: Orijinal belgede <satır> satırındaki tutar, miktar × birim fiyat ile tutmuyor. Excel'e belgede yazdığı gibi aktardım.
```

## Teslim — Discord
```
Botunuz hazır, ekteki zip'te. İçindeki KURULUM.md dosyası adım adım anlatıyor, kurulum yaklaşık 15 dakika sürer. Kısaca: bot hesabı oluşturup token'ı .env dosyasına yazıyorsunuz, "pip install -r requirements.txt" ve "python bot.py" çalıştırıyorsunuz. Sonra panelleri /ticket-panel ve /kayit-panel komutlarıyla kuruyorsunuz. Takıldığınız yerde ekran görüntüsü atın, yardımcı olurum.
```

## Yorum isteği (onaydan sonra, bir kez)
```
Siparişiniz onaylandı, teşekkür ederim. Memnun kaldıysanız kısa bir yorum bırakmanız bana çok yardımcı olur.
```

## Ödev reddi
```
Merhaba, ilginiz için teşekkürler. Bionluk kuralları gereği okul ödevi ve proje ödevi hizmeti veremiyorum, kusura bakmayın.
```

## Kapsam dışı
```
Merhaba, bu istek ilanımın kapsamında değil, bu yüzden almam doğru olmaz. İlanımdaki <hizmet> için her zaman buradayım.
```
