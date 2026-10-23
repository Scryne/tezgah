"""İlan kapakları: HTML -> PNG (1280x720). Kanıt görselleri gerçek çıktıdan: S1 taranmış fatura + aynı faturanın tablosu."""
import base64
import io
import json
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

KOK = Path(__file__).resolve().parents[3]
S1 = KOK / "spikes/s1-donusturme/veri"
OUT = Path(__file__).parent

def tarama_kirp():
    im = Image.open(S1 / "b_fatura_tarama_s1.jpg").crop((150, 150, 1030, 870))
    b = io.BytesIO(); im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

ORTAK = """
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--zemin:#101826;--zemin-acik:#1B2638;--murekkep:#F4F1EA;--soluk:#9AA7B8;--vurgu:#F2A93B;--dogru:#3FB97A;--kagit:#F7F5F0;--discord:#5865F2}
*{box-sizing:border-box;margin:0}
body{width:1280px;height:720px;background:radial-gradient(1200px 700px at 0% 0%,#1F2C42 0%,var(--zemin) 60%);color:var(--murekkep);
 font-family:Inter,sans-serif;display:grid;grid-template-columns:500px 1fr;gap:40px;padding:64px 56px 56px 64px;overflow:hidden}
h1{font-family:'Inter Tight';font-weight:800;font-size:60px;line-height:1.04;letter-spacing:-.02em}
h1 em{font-style:normal;color:var(--vurgu)}
ul{list-style:none;padding:0;margin-top:34px;display:grid;gap:16px}
li{font-size:23px;font-weight:500;color:#DCE3EC;display:flex;gap:12px;align-items:baseline}
body>div:first-child{align-self:center;margin-top:-40px}
li::before{content:"";flex:none;width:10px;height:10px;border-radius:2px;background:var(--vurgu);transform:translateY(-3px)}
.alt{position:absolute;left:64px;bottom:52px;font-size:18px;color:var(--soluk);font-weight:600}
.damga{display:inline-flex;align-items:center;gap:8px;background:rgba(63,185,122,.14);border:1px solid rgba(63,185,122,.55);
 color:#7FE0AE;font-weight:600;font-size:17px;padding:8px 14px;border-radius:999px}
</style>"""

def donustur_html():
    g = json.loads((S1 / "b_fatura.json").read_text(encoding="utf-8"))
    secili = list(enumerate(g["satirlar"]))[:8] + list(enumerate(g["satirlar"]))[-3:]  # gerçek satır numaralarıyla
    tr = "".join(
        ("<tr><td class=n>…</td>" + "<td>…</td>" * 6 + "</tr>" if i == len(g["satirlar"]) - 3 else "")
        + f"<tr><td class=n>{i+2}</td>" + "".join(
            f"<td class='{'r' if j>=3 and c[:1].isdigit() else ''} {'t' if r[0]=='' and j>=4 else ''}'>{c}</td>" for j, c in enumerate(r)) + "</tr>"
        for i, r in secili)
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
.sag{{position:relative}}
.once{{position:absolute;left:0;top:10px;width:330px;border-radius:10px;box-shadow:0 20px 40px rgba(0,0,0,.45);transform:rotate(-3deg);filter:grayscale(.2)}}
.ok{{position:absolute;left:300px;top:250px;font:800 54px 'Inter Tight';color:var(--vurgu)}}
.excel{{position:absolute;right:0;top:120px;width:560px;background:#fff;color:#1d2733;border-radius:10px;overflow:hidden;
 box-shadow:0 24px 50px rgba(0,0,0,.5);font-size:11.5px}}
.excel .bar{{background:#1E7145;color:#fff;font:600 13px Inter;padding:8px 12px}}
table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #DADDE1;padding:4px 6px;white-space:nowrap}}
td.t:not(.r){{text-align:right}}
th{{background:#F2F3F5;font-weight:600;color:#566;font-size:10.5px}}
td.n{{background:#F2F3F5;color:#778;text-align:center;width:22px}}
td.r{{text-align:right;font-family:'JetBrains Mono';font-size:11px}}
td.t{{font-weight:700}}
tr.h td{{font-weight:700;background:#F7FAF8}}
.sag .damga{{position:absolute;right:0;bottom:0}}
</style><body>
<div><h1>PDF ve taranmış belge <em>Excel'e</em></h1>
<ul><li>Fatura, fiyat listesi, stok listesi</li><li>Fotoğraf ve taranmış sayfa da olur</li><li>Rakamlar Excel'de hesaplanabilir sayı</li></ul></div>
<div class=sag><img class=once src="{tarama_kirp()}"><div class=ok>→</div>
<div class=excel><div class=bar>fatura.xlsx</div><table><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>
<tr class=h><td class=n>1</td>{"".join(f"<td>{h}</td>" for h in g["basliklar"])}</tr>{tr}</table></div>
<span class=damga>✓ Toplamlar teslimden önce kontrol edilir</span></div>
<div class=alt>1 günde teslim · Türkçe karakter korunur</div></body>"""

def discord_html():
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
.sag{{position:relative}}
.pencere{{position:absolute;right:0;top:0;width:560px;background:#313338;border-radius:14px;padding:22px 24px;box-shadow:0 24px 50px rgba(0,0,0,.5);
 font-family:Inter;color:#DBDEE1}}
.msg{{display:grid;grid-template-columns:44px 1fr;gap:14px;margin-bottom:20px}}
.av{{width:44px;height:44px;border-radius:50%;background:var(--discord);display:grid;place-items:center;font:800 18px 'Inter Tight';color:#fff}}
.ad{{font-weight:600;color:#fff;font-size:15px}} .ad b{{background:var(--discord);font-size:10px;padding:1px 5px;border-radius:4px;margin-left:6px;vertical-align:2px}}
.embed{{margin-top:6px;background:#2B2D31;border-left:4px solid var(--discord);border-radius:4px;padding:12px 14px;font-size:14px;line-height:1.45}}
.embed h3{{color:#fff;font-size:15px;margin-bottom:4px}}
.btn{{display:inline-block;margin-top:10px;margin-right:8px;padding:8px 14px;border-radius:4px;font-weight:600;font-size:14px;color:#fff}}
.yesil{{background:#248046}} .mavi{{background:var(--discord)}} .kirmizi{{background:#DA373C}}
.log{{font-size:13.5px;color:#B5BAC1;line-height:1.6}} .log span{{color:#C9CDFB}}
.sag .damga{{position:absolute;right:0;bottom:0}}
</style><body>
<div><h1>Ticket, kayıt ve moderasyon <em>botu</em></h1>
<ul><li>Hazır ve test edilmiş modüller</li><li>Sunucunuza özel ayarlı, Türkçe</li><li>Adım adım kurulum rehberi</li></ul></div>
<div class=sag><div class=pencere>
<div class=msg><div class=av>B</div><div><div class=ad>Botunuz<b>BOT</b></div>
<div class=embed><h3>Destek</h3>Bir sorunun mu var? Aşağıdaki düğmeyle destek talebi aç, ekibimiz yardımcı olsun.</div>
<span class="btn yesil">🎫 Destek Talebi Aç</span></div></div>
<div class=msg><div class=av>B</div><div><div class=ad>Botunuz<b>BOT</b></div>
<div class=embed><h3>Kayıt</h3>Sunucuya erişmek için aşağıdaki düğmeyle kaydını tamamla.</div>
<span class="btn mavi">📝 Kayıt Ol</span></div></div>
<div class=msg><div class=av>B</div><div><div class=ad>Botunuz<b>BOT</b></div>
<div class=log>Kayıt: <span>@yeni_uye</span> → Ahmet | 19<br>Uyarı: <span>@spamci</span> (3. uyarı) — 60 dk susturuldu<br>Talep kapandı: destek-mert — döküm kaydedildi</div></div></div>
</div><span class=damga>✓ 1 günde teslim</span></div>
<div class=alt>/ban /at /sustur /temizle /uyar · bağlantı ve spam engeli</div></body>"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(Path.home() / "AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe"))
    for ad, html in [("kapak-donustur", donustur_html()), ("kapak-discord", discord_html())]:
        (OUT / f"{ad}.html").write_text(html, encoding="utf-8")
        s = b.new_page(viewport={"width": 1280, "height": 720})
        s.goto((OUT / f"{ad}.html").as_uri()); s.wait_for_timeout(1500)
        s.screenshot(path=str(OUT / f"{ad}.png"))
        print(ad, "ok")
    b.close()
