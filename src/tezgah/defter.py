"""Sipariş defteri: öldürme kriteri (yayından 30 gün sonra 0 sipariş) ve fiyat kararı için ölçüm.
Müşteri adı yazılmaz; gerekiyorsa Bionluk sipariş numarası nota girer."""
import csv
import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path

ALANLAR = ["tarih", "hizmet", "paket", "tutar_tl", "net_tl", "not"]
KOMISYON = 0.20  # Bionluk, KDV ve banka dahil (araştırma 2026-10-23)
OLDURME_GUN = 30


@dataclass
class Ozet:
    siparis: int
    brut: float
    net: float
    yayin: dt.date | None
    gun: int | None

    @property
    def oldurme(self) -> bool:
        return self.gun is not None and self.gun >= OLDURME_GUN and self.siparis == 0


class Defter:
    def __init__(self, klasor: Path):
        self.csv = klasor / "defter.csv"
        self.durum = klasor / "durum.json"

    def ekle(self, hizmet: str, tutar: float, paket: str = "", not_: str = "", tarih: dt.date | None = None) -> dict:
        satir = {"tarih": (tarih or dt.date.today()).isoformat(), "hizmet": hizmet, "paket": paket,
                 "tutar_tl": f"{tutar:.2f}", "net_tl": f"{tutar * (1 - KOMISYON):.2f}", "not": not_}
        yeni = not self.csv.exists()
        self.csv.parent.mkdir(parents=True, exist_ok=True)
        with self.csv.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=ALANLAR)
            if yeni:
                w.writeheader()
            w.writerow(satir)
        return satir

    def satirlar(self) -> list[dict]:
        if not self.csv.exists():
            return []
        with self.csv.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def yayin_ayarla(self, tarih: dt.date) -> None:
        self.durum.parent.mkdir(parents=True, exist_ok=True)
        self.durum.write_text(json.dumps({"yayin": tarih.isoformat()}), encoding="utf-8")

    def ozet(self, bugun: dt.date | None = None) -> Ozet:
        s = self.satirlar()
        yayin = None
        if self.durum.exists():
            yayin = dt.date.fromisoformat(json.loads(self.durum.read_text(encoding="utf-8"))["yayin"])
        gun = ((bugun or dt.date.today()) - yayin).days if yayin else None
        return Ozet(len(s), sum(float(r["tutar_tl"]) for r in s), sum(float(r["net_tl"]) for r in s), yayin, gun)
