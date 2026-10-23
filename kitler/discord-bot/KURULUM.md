# Discord Botu — Kurulum

Bu paket senin sunucuna özel ayarlanmış hazır bir bottur. Kurulum bir kez yapılır, yaklaşık 15 dakika sürer.

## 1. Bot hesabını oluştur
1. https://discord.com/developers/applications adresinde **New Application** de, bir ad ver.
2. Soldan **Bot** sekmesi: **Reset Token** ile token'ı al ve bir yere kopyala (kimseyle paylaşma).
3. Aynı sayfada **Privileged Gateway Intents** altında **Server Members Intent** ve **Message Content Intent** seçeneklerini aç, kaydet.
4. Soldan **OAuth2 > URL Generator**: `bot` ve `applications.commands` kutularını, izinlerde **Administrator**'ı seç.
   Çıkan bağlantıyı tarayıcıda aç ve botu sunucuna ekle.
5. Sunucu ayarları > Roller: botun rolünü, vereceği rollerin (kayıtsız, üye) **üstüne** sürükle. Yoksa rol veremez.

## 2. Bilgisayara ya da sunucuya kur
1. Python 3.10 veya üstü kur (https://www.python.org/downloads/, kurulumda "Add to PATH" işaretli).
2. Bu klasörde bir terminal aç:
   ```
   pip install -r requirements.txt
   ```
3. `.env.ornek` dosyasını `.env` adıyla kopyala, `DISCORD_TOKEN=` satırına token'ı yapıştır.
4. `ayar.yaml` senin sunucuna göre doldurulmuş olarak geldi. Bir kimliği değiştirmek istersen: Discord > Ayarlar > Gelişmiş >
   Geliştirici Modu açık; kanal, rol ya da sunucuya sağ tık > **ID'yi Kopyala**.

## 3. Çalıştır
```
python bot.py
```
Terminalde `Bağlandı: <bot adı>` görünce hazır. Bot, bu pencere açık kaldığı sürece çalışır; 7/24 çalışması için
bilgisayarın açık kalmalı ya da botu bir VPS'e (Linux sunucu) aynı adımlarla kurmalısın.

## 4. Panelleri kur
- Destek kanalında `/ticket-panel`, kayıt kanalında `/kayit-panel` yaz. Paneller kalıcıdır, bot yeniden başlasa da çalışır.

## Komutlar
| Komut | Ne yapar | Kim kullanır |
| --- | --- | --- |
| `/ticket-panel`, `/kayit-panel` | Paneli bulunduğun kanala koyar | Sunucu yöneticisi |
| `/ban`, `/at` | Yasaklar, atar | Yetkili rolü |
| `/sustur <üye> <dakika>` | Susturur (en çok 28 gün) | Yetkili rolü |
| `/temizle <adet>` | Son mesajları siler (en çok 100) | Yetkili rolü |
| `/uyar`, `/uyarilar` | Uyarı verir / geçmişi gösterir; limitte 60 dk susturma | Yetkili rolü |

Yetkili olmayanların bağlantıları silinir, kısa sürede çok mesaj atan susturulur. Hepsi log kanalına yazılır.

## Sorun giderme
- **"ayar.yaml eksik: ..."** — yazan alanın kimliğini ayar.yaml'a gir.
- **Komutlar görünmüyor** — botu `applications.commands` ile eklediğinden emin ol, Discord'u yenile (Ctrl+R).
- **Rol veremiyor / takma ad değiştiremiyor** — botun rolü verilen rollerin üstünde olmalı. Sunucu sahibinin takma adı botla değişmez.
