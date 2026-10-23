"""Türkçe sayı biçimi: '1.234,56' <-> 1234.56. Kod gibi duran metinler (baştaki sıfır, harf) sayıya çevrilmez."""
import re

_TR = re.compile(r"^-?(\d{1,3}(\.\d{3})+|\d+)(,\d+)?$")


def sayi_mi(metin: str) -> bool:
    s = (metin or "").strip()
    if not _TR.match(s):
        return False
    rakamlar = s.lstrip("-")
    # "0110" gibi baştaki sıfır kod/numaradır, "0,50" sayıdır
    return not (len(rakamlar) > 1 and rakamlar[0] == "0" and rakamlar[1] != ",")


def coz(metin: str) -> float | None:
    if not sayi_mi(metin):
        return None
    return float(metin.strip().replace(".", "").replace(",", "."))


def ondalik_basamak(metin: str) -> int:
    s = metin.strip()
    return len(s.split(",")[1]) if "," in s else 0


def bicimle(x: float, basamak: int = 2) -> str:
    s = f"{x:,.{basamak}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def kucult(metin: str) -> str:
    """Türkçe küçük harf: 'TOPLAM', 'İade', 'KDV' karşılaştırması için."""
    return (metin or "").replace("İ", "i").replace("I", "ı").lower()
