"""Tezgah: freelance teslim kitleri."""
import os
from pathlib import Path


def proje_koku() -> Path:
    """`calisma/` ve `veri/` deponun kökünde durur: komut başka bir klasörden koşsa da siparişler ve defter yerinde
    kalır (önceden `Path.cwd()` tabanlıydı, yanlış klasörde sessizce yeni bir defter açılıyordu). `TEZGAH_KOK` ezer."""
    if ortam := os.environ.get("TEZGAH_KOK"):
        return Path(ortam)
    kok = Path(__file__).resolve().parents[2]  # src/tezgah/ → depo kökü (uv'nin düzenlenebilir kurulumu)
    return kok if (kok / "pyproject.toml").is_file() else Path.cwd()
