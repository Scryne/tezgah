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

def otomasyon_html():
    adimlar = [("Konu seçimi ve senaryo", "yapay zekâ", "12 sn"), ("Seslendirme", "Türkçe ses", "21 sn"),
               ("Görsel ve kurgu", "9:16 video", "48 sn"), ("Kontrol", "süre, ses, altyazı", "3 sn"),
               ("Planlı yayın", "takvime göre", "6 sn"), ("Bildirim", "Telegram", "1 sn")]
    satir = "".join(f"<div class=adim><span class=tik>✓</span><b>{a}</b><i>{b}</i><em>{c}</em></div>" for a, b, c in adimlar)
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
.sag{{position:relative}}
.kart{{position:absolute;right:0;top:20px;width:560px;background:#151F2E;border:1px solid rgba(255,255,255,.08);border-radius:16px;
 padding:22px 24px;box-shadow:0 24px 50px rgba(0,0,0,.5)}}
.ust{{display:flex;justify-content:space-between;color:var(--soluk);font:600 14px Inter;margin-bottom:14px}}
.ust b{{color:var(--murekkep)}}
.adim{{display:grid;grid-template-columns:28px 1fr auto 60px;gap:12px;align-items:center;padding:11px 0;border-top:1px solid rgba(255,255,255,.06);font-size:16px}}
.adim b{{font-weight:600}} .adim i{{font-style:normal;color:var(--soluk);font-size:14px}}
.adim em{{font-style:normal;font-family:'JetBrains Mono';font-size:13px;color:var(--soluk);text-align:right}}
.tik{{color:var(--dogru);font-weight:800}}
.not{{margin-top:10px;font-size:12px;color:var(--soluk)}}
.sag .damga{{position:absolute;right:0;bottom:0}}
</style><body>
<div><h1>İşinizi <em>otomatik</em> çalışan sisteme çeviriyorum</h1>
<ul><li>Python ve yapay zekâ servisleri</li><li>Bulutta, zamanlanmış, bildirimli</li><li>Kaynak kod ve doküman sizde</li></ul></div>
<div class=sag><div class=kart><div class=ust><b>Her gün 09:00 · otomatik</b><span>örnek akış</span></div>{satir}
<div class=not>Hata olursa yeniden dener, düzelmezse haber verir.</div></div>
<span class=damga>✓ Kapsam ve aylık gider baştan yazılı</span></div>
<div class=alt>İçerik üretimi · ofis işleri · API bağlantıları · bildirim botları</div></body>"""


def fiverr_html():
    adimlar = [("Topic & script", "AI", "12 s"), ("Voice-over", "TTS", "21 s"), ("Visuals & edit", "9:16 video", "48 s"),
               ("Quality check", "length, audio, captions", "3 s"), ("Scheduled publish", "on your calendar", "6 s"),
               ("Notification", "Telegram", "1 s")]
    satir = "".join(f"<div class=adim><span class=tik>✓</span><b>{a}</b><i>{b}</i><em>{c}</em></div>" for a, b, c in adimlar)
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
body{{height:769px}}
.sag{{position:relative}}
.kart{{position:absolute;right:0;top:30px;width:560px;background:#151F2E;border:1px solid rgba(255,255,255,.08);border-radius:16px;
 padding:22px 24px;box-shadow:0 24px 50px rgba(0,0,0,.5)}}
.ust{{display:flex;justify-content:space-between;color:var(--soluk);font:600 14px Inter;margin-bottom:14px}}
.ust b{{color:var(--murekkep)}}
.adim{{display:grid;grid-template-columns:28px 1fr auto 50px;gap:12px;align-items:center;padding:11px 0;border-top:1px solid rgba(255,255,255,.06);font-size:16px}}
.adim b{{font-weight:600}} .adim i{{font-style:normal;color:var(--soluk);font-size:14px}}
.adim em{{font-style:normal;font-family:'JetBrains Mono';font-size:13px;color:var(--soluk);text-align:right}}
.tik{{color:var(--dogru);font-weight:800}}
.not{{margin-top:10px;font-size:12px;color:var(--soluk)}}
.sag .damga{{position:absolute;right:0;bottom:0}}
</style><body>
<div><h1>Turn repetitive work into an <em>automated</em> system</h1>
<ul><li>Python + AI services</li><li>Runs in the cloud, on schedule</li><li>You own the code and the docs</li></ul></div>
<div class=sag><div class=kart><div class=ust><b>Every day 09:00 · automatic</b><span>sample pipeline</span></div>{satir}
<div class=not>Retries on failure, alerts you if it still fails.</div></div>
<span class=damga>✓ Scope and monthly costs agreed upfront</span></div>
<div class=alt>Content pipelines · office automation · API integrations · alert bots</div></body>"""


def trendyol_html():
    once = [("Başlık", "İNCİLİ KOLYE"), ("Özellikler", "2 / 9 alan dolu"), ("Açıklama", "yok")]
    sonra = [("Başlık", "Kadın El Yapımı İnci Kolye Deniz Kabuğu Charmlı İnce Zincir"), ("Özellikler", "9 / 9 alan dolu"),
             ("Açıklama", "malzeme, ölçü, kullanım, bakım, paket")]
    def kart(sinif, etiket, satirlar):
        return (f"<div class='kart {sinif}'><div class=ust>{etiket}</div>"
                + "".join(f"<div class=satir><i>{a}</i><b>{b}</b></div>" for a, b in satirlar) + "</div>")
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
.sag{{position:relative;display:flex;flex-direction:column;gap:18px;justify-content:center;margin-top:-30px}}
.kart{{border-radius:16px;padding:18px 22px;box-shadow:0 24px 50px rgba(0,0,0,.45)}}
.kart.once{{background:#1B2638;border:1px solid rgba(255,255,255,.08);color:var(--soluk);width:470px;transform:rotate(-1.5deg)}}
.kart.sonra{{background:var(--kagit);color:#1d2733;margin-left:60px}}
.ust{{font:800 13px Inter;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px}}
.once .ust{{color:#7D8A9C}} .sonra .ust{{color:#1E7145}}
.satir{{display:grid;grid-template-columns:110px 1fr;gap:12px;padding:8px 0;border-top:1px solid rgba(128,128,128,.18);font-size:16px}}
.satir i{{font-style:normal;font-size:14px;opacity:.75}} .satir b{{font-weight:600}}
.once .satir b{{font-family:'JetBrains Mono';font-weight:500}}
.sag .damga{{align-self:flex-end}}
</style><body>
<div><h1>Trendyol ürünleriniz <em>satışa hazır</em></h1>
<ul><li>Başlık, açıklama ve eksik özellikler</li><li>Toplu yüklemeye hazır Excel</li><li>Bilmediğimi sorarım, uydurmam</li></ul></div>
<div class=sag>{kart("once", "Önce", once)}{kart("sonra", "Sonra", sonra)}
<span class=damga>✓ İlk ürünü ücretsiz düzenleyip gösteririm</span></div>
<div class=alt>Takı · giyim · aksesuar · ev tekstili · Hepsiburada da olur</div></body>"""


def portfolyo_trendyol_html():
    """Temsili ürün; 'önce' sütunu 10-28'de Trendyol'da görülen gerçek kusur tipinden (büyük harf başlık, 2 alan, açıklama yok)."""
    sonra_ozellik = [("Taş Cinsi", "İnci"), ("Renk", "Beyaz / Altın"), ("Materyal", "Paslanmaz Çelik"), ("Kaplama", "Altın Kaplama"),
                     ("Zincir Uzunluğu", "45 cm"), ("Uzatma Zinciri", "5 cm"), ("Tarz", "Günlük"), ("Menşei", "TR"), ("Kutu Durumu", "Kutulu")]
    once_ozellik = [("Renk", "Beyaz"), ("Menşei", "TR")]
    tablo = lambda xs: "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in xs)
    return f"""<!doctype html><meta charset=utf-8>{ORTAK}<style>
body{{display:flex;flex-direction:column;justify-content:center;padding:44px 56px}}
body>div.bas{{display:flex;justify-content:space-between;align-items:baseline;margin:0 0 22px;align-self:stretch}}
.bas h2{{font:800 30px 'Inter Tight'}} .bas span{{color:var(--soluk);font:600 15px Inter}}
.iki{{display:grid;grid-template-columns:1fr 1.35fr;gap:26px}}
.k{{border-radius:14px;padding:18px 20px}}
.k.once{{background:#1B2638;border:1px solid rgba(255,255,255,.08);color:#C9D2DE}}
.k.sonra{{background:var(--kagit);color:#1d2733}}
.et{{font:800 12px Inter;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}}
.once .et{{color:#7D8A9C}} .sonra .et{{color:#1E7145}}
h3{{font:700 18px Inter;line-height:1.3;margin-bottom:12px}}
.once h3{{font-family:'JetBrains Mono';font-weight:500;font-size:17px}}
.alt-b{{font:700 12px Inter;text-transform:uppercase;letter-spacing:.06em;opacity:.6;margin:12px 0 6px}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}
td{{padding:5px 8px;border-top:1px solid rgba(128,128,128,.2)}} td:first-child{{opacity:.7;width:42%}}
p.ac{{font-size:13.5px;line-height:1.5}}
.yok{{font-family:'JetBrains Mono';font-size:14px;opacity:.7}}
.sonra .cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.not{{margin-top:14px;font-size:13px;color:var(--soluk)}}
</style><body>
<div class=bas><h2>Trendyol ürün düzenleme · örnek çalışma</h2><span>Temsili ürün · bijuteri kolye</span></div>
<div class=iki>
<div class='k once'><div class=et>Önce</div><h3>İNCİLİ KOLYE</h3>
<div class=alt-b>Özellikler · 2 / 9 alan</div><table>{tablo(once_ozellik)}</table>
<div class=alt-b>Açıklama</div><p class=yok>— boş —</p></div>
<div class='k sonra'><div class=et>Sonra</div><h3>Kadın El Yapımı İnci Kolye Deniz Kabuğu Charmlı İnce Zincir 45 cm</h3>
<div class=cols><div><div class=alt-b>Özellikler · 9 / 9 alan</div><table>{tablo(sonra_ozellik)}</table></div>
<div><div class=alt-b>Açıklama</div><p class=ac>El yapımı inci kolye, deniz kabuğu charmı ve ince zinciriyle günlük kullanıma uygun.<br>
• Materyal: paslanmaz çelik zincir, altın kaplama<br>• Uzunluk: 45 cm + 5 cm uzatma zinciri<br>
• Kullanım: suyla ve parfümle temastan kaçının<br>• Bakım: kuru, yumuşak bezle silin<br>• Paket: hediye kutusunda gönderilir</p></div></div></div>
</div>
<div class=not>Materyal ve ölçü gibi bilgiler satıcıdan alınır; bilinmeyen bilgi uydurulmaz. Teslim: toplu güncelleme Excel'i + kopyala-yapıştır metin.</div>
</body>"""


import sys

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(Path.home() / "AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe"))
    hepsi = [("kapak-donustur", donustur_html), ("kapak-discord", discord_html), ("kapak-otomasyon", otomasyon_html),
             ("fiverr-gig", fiverr_html), ("kapak-trendyol", trendyol_html), ("portfolyo-trendyol", portfolyo_trendyol_html)]
    for ad, html in [(a, f()) for a, f in hepsi if not sys.argv[1:] or a in sys.argv[1:]]:
        (OUT / f"{ad}.html").write_text(html, encoding="utf-8")
        s = b.new_page(viewport={"width": 1280, "height": 769 if ad.startswith("fiverr") else 720})
        s.goto((OUT / f"{ad}.html").as_uri()); s.wait_for_timeout(1500)
        s.screenshot(path=str(OUT / f"{ad}.png"))
        print(ad, "ok")
    b.close()
