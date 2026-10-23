import datetime as dt

from tezgah.defter import Defter


def test_defter_net_ve_ozet(tmp_path):
    d = Defter(tmp_path)
    d.ekle("donustur", 250, "standart", tarih=dt.date(2026, 11, 1))
    d.ekle("discord", 600, "standart", tarih=dt.date(2026, 11, 3))
    o = d.ozet()
    assert (o.siparis, o.brut, o.net) == (2, 850, 680)
    assert o.yayin is None and not o.oldurme


def test_oldurme_kriteri_30_gun_sifir_siparis(tmp_path):
    d = Defter(tmp_path)
    d.yayin_ayarla(dt.date(2026, 11, 1))
    assert not d.ozet(dt.date(2026, 11, 30)).oldurme  # 29. gün
    assert d.ozet(dt.date(2026, 12, 1)).oldurme
    d.ekle("donustur", 100)
    assert not d.ozet(dt.date(2026, 12, 1)).oldurme
