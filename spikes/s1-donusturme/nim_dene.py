import base64, json, os, re, sys, time
from pathlib import Path
import httpx
from ortak import puanla

KEY = os.environ["NK"]; MODEL = sys.argv[1]
ISTEM = ("Bu taranmış belgedeki tabloyu birebir çıkar. Yalnızca JSON döndür: {\"satirlar\": [[hücre, ...], ...]}. "
         "Başlık satırını da ekle. Hücre metnini olduğu gibi yaz: Türkçe karakterleri (ç ğ ı İ ö ş ü), sembolleri (Ø), "
         "sayı biçimini (1.234,56) değiştirme. Boş hücre için \"\" yaz. Tahmin etme, okuyamadığın hücreye \"??\" yaz.")
cli = httpx.Client(timeout=300)
def sor(yol):
    b = base64.b64encode(Path(yol).read_bytes()).decode()
    r = cli.post("https://integrate.api.nvidia.com/v1/chat/completions", headers={"Authorization": f"Bearer {KEY}"},
                 json={"model": MODEL, "temperature": 0, "max_tokens": 8000,
                       "messages": [{"role": "user", "content": [{"type": "text", "text": ISTEM},
                                     {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b}"}}]}]})
    r.raise_for_status(); m = r.json()["choices"][0]["message"]
    txt = m.get("content") or ""
    j = re.search(r"\{.*\}", txt, re.S)
    return json.loads(j.group(0))["satirlar"] if j else []
for ad, sayfalar in [("a_fiyat_listesi", 1), ("b_fatura", 1), ("c_uzun_iki_sayfa", 2)]:
    t = time.time(); rows = []
    try:
        for s in range(1, sayfalar + 1): rows += sor(f"veri/{ad}_tarama_s{s}.jpg")
    except Exception as e:
        print(MODEL, ad, "HATA", str(e)[:200]); continue
    i, n, h = puanla(ad, rows)
    print(f"{MODEL} {ad}: {i}/{n} = {i/n:.1%}  {time.time()-t:.1f}s", h[:4], flush=True)
