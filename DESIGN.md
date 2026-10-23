---
version: alpha
name: Tezgah
description: Bionluk ilan kapak görselleri (statik PNG); ürün arayüzü yok, tek görsel yüzey ilan vitrini.
colors:
  zemin: "#101826"
  zemin-acik: "#1B2638"
  murekkep: "#F4F1EA"
  soluk: "#9AA7B8"
  vurgu: "#F2A93B"
  dogru: "#3FB97A"
  kagit: "#F7F5F0"
  discord: "#5865F2"
typography:
  baslik:
    fontFamily: Inter Tight
    fontWeight: 800
    fontSize: 64px
    lineHeight: 1.05
  govde:
    fontFamily: Inter
    fontWeight: 500
    fontSize: 24px
  rakam:
    fontFamily: JetBrains Mono
    fontWeight: 500
    fontSize: 18px
rounded:
  kart: 18px
---

# Tezgah

## Overview

Tek görsel yüzey Bionluk'taki ilan kartı: beyaz liste ızgarasında küçük bir küçük resim olarak görülür, sonra ilan
sayfasında büyük. Kapak iki şeyi bir bakışta söylemeli: ne alınıyor, neden bu satıcı.

- **Mood:** usta tezgâhı — sade, işini bilen, abartısız. Koyu mürekkep zemin, beyaz liste ızgarasında öne çıkar.
- **Farklılaştırıcı detay:** kontrol işareti. Rakiplerin vaat etmediği şey (toplamların kontrolü, hazır test edilmiş modüller)
  görselde yeşil bir "kontrol edildi" damgası olarak durur.

Glassmorphism kullanılmaz: statik PNG'de blur'un arkasında hareket yok, küçük resimde okunabilirliği düşürür (global varsayılanı ezer).

## Colors

Zemin koyu lacivert-mürekkep; tek sıcak vurgu (amber) başlıkta yalnız bir kelimede. Yeşil yalnız doğrulama anlamında.
Discord kapağında Discord'un kendi arayüz renkleri yalnız bot panelinin canlandırmasında; Discord logosu kullanılmaz.

## Typography

Başlık Inter Tight 800, küçük resimde de okunacak boyda ve en fazla iki satır. Tablolardaki rakamlar mono, sağa hizalı.

## Components

- Kapak 1280×720. Sol yarı başlık + 3 kısa madde, sağ yarı tek kanıt görseli (önce→sonra ya da bot paneli).
- Kanıt görseli gerçek çıktıdan gelir (S1 test belgesi, kitin panel metinleri); uydurma ekran yok.

## Do's and Don'ts

- Do: başlık küçük resimde (320 px genişlik) okunur olmalı.
- Don't: iletişim bilgisi, kullanıcı adı, "garanti", "%100" iddiası, Bionluk/Discord logosu.
