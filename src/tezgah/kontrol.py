"""Teslim öncesi kontroller: iki bağımsız okumanın karşılaştırması ve tablonun kendi aritmetiği.
Amaç yanlış rakamı teslim etmemek; her bulgu Claude'un görüntüye bakıp düzeltmesi ya da doğrulaması içindir."""
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from itertools import permutations

from .sayi import coz, kucult


@dataclass
class Bulgu:
    tur: str  # "uyusmazlik" | "carpim" | "toplam" | "bicim"
    kaynak: str
    sayfa: int
    satir: int  # tablodaki 0 tabanlı satır
    sutun: int
    deger: str
    aciklama: str

    def anahtar(self) -> tuple:
        return (self.kaynak, self.sayfa, self.satir, self.sutun)


def _katla(metin: str) -> str:
    """Metin hücresi kıyası için: aksan/Türkçe harf, büyük-küçük ve tırnak farkı yok sayılır, kelime sırası sabitlenir."""
    s = kucult(metin).translate(str.maketrans("ıøØ", "i00"))
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = re.sub(r"(?<=\d)o|o(?=\d)", "0", s)  # OCR: M1O -> m10
    return " ".join(sorted(re.sub(r"['’`\"]+", "", s).split()))


def _benzer_metin(a: str, b: str) -> bool:
    """İkinci okumanın OCR gürültüsünü (l/I, eksik harf, sıra) tolere eder; metindeki rakamlar birebir olmalı."""
    ka, kb = _katla(a), _katla(b)
    if re.findall(r"\d+", ka) != re.findall(r"\d+", kb):
        return False
    return ka == kb or SequenceMatcher(None, ka, kb).ratio() >= 0.8


def _ayni_var(hucre: str, satir: list[str]) -> bool:
    if hucre in satir:
        return True
    if coz(hucre) is not None:  # sayılar birebir: ikinci okumanın harf hatası rakamı affettirmez
        return False
    return any(_benzer_metin(hucre, x) for x in satir if x and coz(x) is None)


def _anahtar_hucre(satir: list[str]) -> str:
    return next((c for c in satir if c), "")


def karsilastir(birincil: list[dict], ikincil: list[dict]) -> list[Bulgu]:
    """Birincil okumanın (Claude) her dolu hücresi, ikincil okumada (docling) aynı satırda geçiyor mu?
    Satırlar anahtar hücreyle eşlenir; sütun kayması uyuşmazlık sayılmaz, değer farkı sayılır.
    Metin hücrelerinde OCR gürültüsü sayılmaz (S1: docling ş/ğ/ı düşürüyor, kelime sırası kayıyor), sayılar birebir.
    Satırında a × b = c tutan sayı hücresi uyuşmazlık sayılmaz: yanlış okunmuş rakamın çarpımı tutturması pratikte imkânsız,
    hata ikinci okumadadır (S1 uçtan uca: 19 bulgunun 19'u docling'in)."""
    bulgular = []
    for t in birincil:
        guvenli = hesabi_tutan_hucreler(t)
        ikinci_satirlar = [r for u in ikincil if (u["kaynak"], u["sayfa"]) == (t["kaynak"], t["sayfa"]) for r in u["satirlar"]]
        for i, satir in enumerate(t["satirlar"]):
            hucreler = [c for c in satir if c]
            if not hucreler:
                continue
            anahtar = _anahtar_hucre(satir)
            adaylar = [r for r in ikinci_satirlar if anahtar in r] or ikinci_satirlar
            es = max(adaylar, key=lambda r: sum(_ayni_var(c, r) for c in hucreler), default=[])
            for j, c in enumerate(satir):
                if c and (i, j) not in guvenli and not _ayni_var(c, es):
                    gorulen = " | ".join(x for x in es if x)[:100] or "(satır bulunamadı)"
                    bulgular.append(Bulgu("uyusmazlik", t["kaynak"], t["sayfa"], i, j, c, f"ikinci okuma: {gorulen}"))
    return bulgular


def _yakin(a: float, b: float) -> bool:
    return abs(round(a, 2) - b) <= 0.011


def _uclu(sayilar: list[list[float | None]], genislik: int) -> tuple[int, int, int] | None:
    """Satırların çoğunda a × b = c tutan sütun üçlüsü (miktar × birim fiyat = tutar)."""
    en_iyi, destek_en = None, 0
    for a, b, c in permutations(range(genislik), 3):
        if a > b:
            continue
        uclu = [r for r in sayilar if len(r) > max(a, b, c) and None not in (r[a], r[b], r[c])]
        tutan = sum(_yakin(r[a] * r[b], r[c]) for r in uclu)
        if tutan >= 3 and tutan >= 0.6 * len(uclu) and tutan > destek_en:
            en_iyi, destek_en = (a, b, c), tutan
    return en_iyi


def hesabi_tutan_hucreler(tablo: dict) -> set[tuple[int, int]]:
    sayilar = [[coz(c) for c in r] for r in tablo["satirlar"]]
    u = _uclu(sayilar, max((len(r) for r in sayilar), default=0))
    if not u:
        return set()
    a, b, c = u
    return {(i, j) for i, r in enumerate(sayilar)
            if len(r) > max(u) and None not in (r[a], r[b], r[c]) and _yakin(r[a] * r[b], r[c]) for j in u}


def aritmetik(tablo: dict) -> list[Bulgu]:
    """Satırların çoğunda a × b = c tutuyorsa (miktar × birim fiyat = tutar), tutmayan satırı işaretler.
    'Ara toplam', 'KDV %x', 'Genel toplam' satırlarını da hesaplar."""
    satirlar = tablo["satirlar"]
    sayilar = [[coz(c) for c in r] for r in satirlar]
    genislik = max((len(r) for r in satirlar), default=0)
    if genislik < 3:
        return []
    en_iyi = _uclu(sayilar, genislik)

    bulgular = []
    k = tablo["kaynak"], tablo["sayfa"]
    veri_satirlari = []
    if en_iyi:
        a, b, c = en_iyi
        for i, r in enumerate(sayilar):
            if len(r) > max(a, b, c) and None not in (r[a], r[b], r[c]):
                veri_satirlari.append(i)
                if not _yakin(r[a] * r[b], r[c]):
                    bulgular.append(Bulgu("carpim", *k, i, c, satirlar[i][c],
                                          f"{satirlar[i][a]} × {satirlar[i][b]} = {r[a] * r[b]:,.2f} tutmuyor"))

    # Toplam satırları: etiketli satırın son sayısı
    ara = kdv = None
    for i, r in enumerate(satirlar):
        etiket = kucult(" ".join(r))
        if "toplam" not in etiket and "kdv" not in etiket:
            continue
        son = next(((j, sayilar[i][j]) for j in range(len(r) - 1, -1, -1) if sayilar[i][j] is not None), None)
        if not son:
            continue
        j, deger = son
        beklenen = None
        if "genel" in etiket and ara is not None and kdv is not None:
            beklenen = ara + kdv
        elif "kdv" in etiket and ara is not None and (m := re.search(r"%\s*(\d+)", etiket)):
            beklenen, kdv = ara * int(m.group(1)) / 100, deger
        elif "toplam" in etiket and "genel" not in etiket and en_iyi and veri_satirlari:
            beklenen, ara = sum(sayilar[v][en_iyi[2]] for v in veri_satirlari), deger
        if beklenen is not None and not _yakin(beklenen, deger):
            bulgular.append(Bulgu("toplam", *k, i, j, r[j], f"hesaplanan {beklenen:,.2f}"))
    return bulgular


_OZET = ("toplam", "kdv", "iskonto", "yekün", "yekun")


def bicim(tablo: dict) -> list[Bulgu]:
    """Çoğu sayı olan sütunda sayıya çevrilemeyen hücre: '191,08' yerine '191.08' gibi okuma hatası
    sessizce metne dönüşmesin. Toplam/KDV satırlarının etiketleri sayılmaz."""
    satirlar = [r for r in tablo["satirlar"][1:]]
    bulgular = []
    genislik = max((len(r) for r in satirlar), default=0)
    for j in range(genislik):
        hucreler = [(i + 1, r[j]) for i, r in enumerate(satirlar)
                    if j < len(r) and r[j] and not any(o in kucult(" ".join(r)) for o in _OZET)]
        sayisal = [h for h in hucreler if coz(h[1]) is not None]
        if len(sayisal) >= 3 and len(sayisal) >= 0.8 * len(hucreler):
            for i, c in hucreler:
                if coz(c) is None:
                    bulgular.append(Bulgu("bicim", tablo["kaynak"], tablo["sayfa"], i, j, c,
                                          "sayı sütununda sayıya çevrilemiyor (1.234,56 biçimi bekleniyor)"))
    return bulgular


def suz(bulgular: list[Bulgu], dogrulanan: list[dict]) -> list[Bulgu]:
    """Claude'un görüntüye bakıp 'belgede gerçekten böyle' dediği bulguları düşer."""
    tamam = {(d["kaynak"], d["sayfa"], d["satir"], d["sutun"]) for d in dogrulanan}
    return [b for b in bulgular if b.anahtar() not in tamam]
