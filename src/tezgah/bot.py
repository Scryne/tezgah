"""Discord bot kitini müşteriye özel ayarla paketler: kod + ayar.yaml + rehber, tek zip."""
import importlib.util
import zipfile
from pathlib import Path

import yaml

KIT = Path(__file__).resolve().parents[2] / "kitler" / "discord-bot"
DAHIL = ["bot.py", "ayar.py", "requirements.txt", "KURULUM.md", ".env.ornek", "moduller/__init__.py",
         "moduller/ticket.py", "moduller/kayit.py", "moduller/moderasyon.py"]


def _ayar_modulu():
    spec = importlib.util.spec_from_file_location("kit_ayar", KIT / "ayar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def paketle(ayar_yolu: Path, cikti: Path) -> Path:
    """Ayarı kitin kendi doğrulamasından geçirir (eksik kimlikle paket çıkmaz), zip'i yazar."""
    ayar = yaml.safe_load(ayar_yolu.read_text(encoding="utf-8")) or {}
    _ayar_modulu().dogrula(ayar)
    cikti.mkdir(parents=True, exist_ok=True)
    zip_yolu = cikti / f"discord-bot-{ayar_yolu.stem}.zip"
    with zipfile.ZipFile(zip_yolu, "w", zipfile.ZIP_DEFLATED) as z:
        for ad in DAHIL:
            z.write(KIT / ad, f"discord-bot/{ad}")
        z.write(ayar_yolu, "discord-bot/ayar.yaml")
    return zip_yolu
