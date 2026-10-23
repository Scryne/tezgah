"""Ölçüm: çıkarılan tabloyu bilinen cevapla hücre hücre karşılaştırır."""
import json, re, unicodedata
from pathlib import Path

def norm(s):
    s = unicodedata.normalize("NFC", str(s or "")).strip()
    return re.sub(r"\s+", " ", s)

def puanla(ad, satirlar):
    """satirlar: çıkarılan tablo (başlık dahil olabilir). Ürün koduyla eşleştirir, 6 hücreyi kıyaslar."""
    dogru = json.loads(Path(f"veri/{ad}.json").read_text(encoding="utf-8"))
    cikan = [[norm(c) for c in r] for r in satirlar]
    toplam = isabet = 0; hatalar = []
    for g in dogru["satirlar"]:
        g = [norm(c) for c in g]
        anahtar = g[0] or g[4]
        aday = [r for r in cikan if anahtar and anahtar in r]
        r = max(aday, key=lambda r: sum(c in r for c in g), default=[])
        ri = [c for c in r if c]  # boş hücreleri at, sırayı koru
        for c in [c for c in g if c]:
            toplam += 1
            if c in ri: isabet += 1
            elif len(hatalar) < 6: hatalar.append((anahtar, c, " | ".join(ri)[:90]))
    return isabet, toplam, hatalar
