"""Bionluk paneli okuyucu: alıcı isteklerini Scryne'ın oturumuyla salt-okunur çeker.
Giriş bir kez, Scryne'ın kendi elleriyle yapılır (şifre koda ve Claude'a girmez); oturum ayrı bir tarayıcı profilinde durur.
Yalnız okur: teklif, mesaj, tıklama-ile-işlem yok. Günde birkaç okumayla sınırlı tutulur (platformu yormamak için)."""
import datetime as dt
from pathlib import Path

ISTEKLER = "https://bionluk.com/panel/alici-istekleri"
PROFIL = Path.cwd() / "calisma" / ".bionluk-profil"  # gitignore'da; oturum çerezleri burada
KAYIT = Path.cwd() / "calisma" / "istekler"


def _chromium() -> str | None:
    """Makinede kurulu Playwright Chromium'u (indirme gerektirmeden) bulur."""
    kok = Path.home() / "AppData/Local/ms-playwright"
    adaylar = sorted(kok.glob("chromium-*/chrome-win64/chrome.exe"), reverse=True)
    return str(adaylar[0]) if adaylar else None


def _baglam(p, gorunur: bool):
    PROFIL.mkdir(parents=True, exist_ok=True)
    return p.chromium.launch_persistent_context(str(PROFIL), headless=not gorunur, executable_path=_chromium(),
                                                viewport={"width": 1280, "height": 900}, locale="tr-TR")


def giris() -> None:
    """Görünür pencere açar; Scryne giriş yapıp pencereyi kapatınca oturum profilde kalır."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = _baglam(p, gorunur=True)
        s = b.pages[0] if b.pages else b.new_page()
        s.goto(ISTEKLER)  # oturum yoksa Bionluk giriş sayfasına yönlendirir
        s.wait_for_event("close", timeout=0)
        b.close()


def istekler() -> Path:
    """İstek sayfasının metnini (\"Devamını oku\" açılmış hâlde) tarihli dosyaya yazar, yolunu döner."""
    from playwright.sync_api import TimeoutError as ZamanAsimi
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = _baglam(p, gorunur=False)
        s = b.new_page()
        s.goto(ISTEKLER, wait_until="networkidle")
        if "login" in s.url:
            b.close()
            raise PermissionError("Bionluk oturumu yok ya da süresi dolmuş: `tezgah bionluk giris` ile yeniden gir.")
        for d in s.get_by_text("Devamını oku").all():  # yalnız metni genişletir, işlem yapmaz
            try:
                d.click(timeout=2000)
            except ZamanAsimi:
                continue  # görünmeyen bağlantı: metin zaten kısa hâliyle sayfada
        metin = s.inner_text("body")
        b.close()
    KAYIT.mkdir(parents=True, exist_ok=True)
    yol = KAYIT / f"{dt.datetime.now():%Y-%m-%d-%H%M}.txt"
    yol.write_text(metin, encoding="utf-8")
    return yol
