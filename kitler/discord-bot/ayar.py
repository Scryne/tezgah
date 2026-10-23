"""ayar.yaml okuma ve doğrulama. Açık modülün kimlikleri eksikse bot başlamaz, hata Türkçe ve tek tek söylenir."""
from pathlib import Path

import yaml

ZORUNLU = {
    "ticket": ["kategori_id", "destek_rol_id"],
    "kayit": ["kayitsiz_rol_id", "uye_rol_id", "hosgeldin_kanal_id"],
    "moderasyon": ["yetkili_rol_id"],
}


class AyarHatasi(ValueError):
    pass


def oku(yol: str | Path = "ayar.yaml") -> dict:
    yol = Path(yol)
    if not yol.exists():
        raise AyarHatasi(f"{yol} bulunamadı. ayar.ornek.yaml dosyasını ayar.yaml adıyla kopyalayıp doldur.")
    ayar = yaml.safe_load(yol.read_text(encoding="utf-8")) or {}
    dogrula(ayar)
    return ayar


def dogrula(ayar: dict) -> None:
    hatalar = []
    for alan in ("sunucu_id", "log_kanal_id"):
        if not _kimlik(ayar.get(alan)):
            hatalar.append(f"{alan} boş")
    moduller = ayar.get("moduller") or {}
    if not any((m or {}).get("acik") for m in moduller.values()):
        hatalar.append("hiçbir modül açık değil")
    for ad, alanlar in ZORUNLU.items():
        m = moduller.get(ad) or {}
        if m.get("acik"):
            hatalar += [f"moduller.{ad}.{a} boş" for a in alanlar if not _kimlik(m.get(a))]
    if hatalar:
        raise AyarHatasi("ayar.yaml eksik: " + "; ".join(hatalar))


def _kimlik(deger) -> bool:
    return isinstance(deger, int) and deger > 0


def renk(ayar: dict) -> int:
    return int(str(ayar.get("renk", "#5865F2")).lstrip("#"), 16)
