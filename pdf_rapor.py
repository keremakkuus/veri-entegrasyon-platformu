from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from datetime import datetime
import os

os.makedirs("raporlar", exist_ok=True)

LACIVERT = HexColor("#0D2149")
MAVI     = HexColor("#2D5BE3")
ACIK_MAV = HexColor("#E8EEF8")
KIRMIZI  = HexColor("#e74c3c")
YESIL    = HexColor("#27ae60")
TURUNCU  = HexColor("#f39c12")
GRI      = HexColor("#666666")

def pdf_rapor_olustur(hava, depremler, ml_anomaliler, doviz, hava_kalitesi):
    """Kapsamlı PDF raporu oluşturur"""
    dosya = f"raporlar/rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc   = SimpleDocTemplate(dosya, pagesize=A4,
                               topMargin=1.5*cm, bottomMargin=1.5*cm,
                               leftMargin=2*cm, rightMargin=2*cm)

    styles = getSampleStyleSheet()
    elemanlar = []

    # ── Başlık ──────────────────────────────────────
    baslik_stil = ParagraphStyle(
        "baslik", fontSize=18, textColor=white,
        backColor=LACIVERT, spaceAfter=4,
        spaceBefore=0, leftIndent=10, leading=28
    )
    alt_baslik_stil = ParagraphStyle(
        "alt_baslik", fontSize=11, textColor=GRI,
        spaceAfter=20, leftIndent=10
    )
    bolum_stil = ParagraphStyle(
        "bolum", fontSize=13, textColor=white,
        backColor=MAVI, spaceAfter=8, spaceBefore=15,
        leftIndent=8, leading=22
    )
    normal = ParagraphStyle(
        "normal_tr", fontSize=10, textColor=black,
        spaceAfter=4, fontName="Helvetica"
    )

    elemanlar.append(Paragraph("Kurumsal Veri Entegrasyon Platformu", baslik_stil))
    elemanlar.append(Paragraph(
        f"Otomatik Rapor — {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}  |  Gelistirici: Mehmet Kerem Akkus",
        alt_baslik_stil
    ))

    # ── Özet Tablo ──────────────────────────────────
    elemanlar.append(Paragraph("Genel Ozet", bolum_stil))
    ozet_veri = [
        ["Bilgi", "Deger"],
        ["Rapor Tarihi",     datetime.now().strftime("%d.%m.%Y %H:%M")],
        ["Toplam Deprem",    str(len(depremler))],
        ["ML Anomali",       str(len(ml_anomaliler))],
        ["Sicaklik (Konya)", f"{hava.get('sicaklik_C', '-')}C"],
        ["Nem",              f"%{hava.get('nem_%', '-')}"],
        ["Hava Durumu",      str(hava.get('durum', '-'))],
    ]
    ozet_tablo = Table(ozet_veri, colWidths=[7*cm, 10*cm])
    ozet_tablo.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), LACIVERT),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTSIZE",    (0,0), (-1,0), 11),
        ("BACKGROUND",  (0,1), (0,-1), ACIK_MAV),
        ("FONTSIZE",    (0,1), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, ACIK_MAV]),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0), (-1,-1), 8),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    elemanlar.append(ozet_tablo)

    # ── Döviz ───────────────────────────────────────
    elemanlar.append(Paragraph("Doviz Kurlari", bolum_stil))
    doviz_veri = [
        ["Para Birimi", "TL Karsılıgı"],
        ["1 USD", f"{doviz.get('USD_TRY', '-')} TL"],
        ["1 EUR", f"{doviz.get('EUR_TRY', '-')} TL"],
        ["1 GBP", f"{doviz.get('GBP_TRY', '-')} TL"],
    ]
    doviz_tablo = Table(doviz_veri, colWidths=[8.5*cm, 8.5*cm])
    doviz_tablo.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), LACIVERT),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTSIZE",    (0,0), (-1,0), 11),
        ("FONTSIZE",    (0,1), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, ACIK_MAV]),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    elemanlar.append(doviz_tablo)

    # ── Hava Kalitesi ───────────────────────────────
    elemanlar.append(Paragraph("Hava Kalitesi (Konya)", bolum_stil))
    kalite_veri = [
        ["Parametre", "Deger", "Birim"],
        ["PM10",      str(hava_kalitesi.get("pm10", "-")),  "ug/m3"],
        ["PM2.5",     str(hava_kalitesi.get("pm2_5", "-")), "ug/m3"],
        ["NO2",       str(hava_kalitesi.get("no2", "-")),   "ug/m3"],
        ["Ozon",      str(hava_kalitesi.get("ozon", "-")),  "ug/m3"],
        ["Genel Kalite", str(hava_kalitesi.get("kalite", "-")), ""],
    ]
    kalite_tablo = Table(kalite_veri, colWidths=[6*cm, 6*cm, 5*cm])
    kalite_tablo.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), LACIVERT),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTSIZE",    (0,0), (-1,0), 11),
        ("FONTSIZE",    (0,1), (-1,-1), 10),
        ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, ACIK_MAV]),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    elemanlar.append(kalite_tablo)

    # ── ML Anomaliler ───────────────────────────────
    if ml_anomaliler:
        elemanlar.append(Paragraph("ML Anomali Tespiti", bolum_stil))
        ml_veri = [["Yer", "Buyukluk", "Derinlik", "Aciklama"]]
        for a in ml_anomaliler:
            ml_veri.append([
                str(a.get("yer", ""))[:40],
                f"M{a.get('buyukluk', '')}",
                f"{a.get('derinlik', '')} km",
                str(a.get("aciklama", ""))[:35],
            ])
        ml_tablo = Table(ml_veri, colWidths=[6*cm, 2.5*cm, 2.5*cm, 6*cm])
        ml_tablo.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0), KIRMIZI),
            ("TEXTCOLOR",   (0,0), (-1,0), white),
            ("FONTSIZE",    (0,0), (-1,-1), 9),
            ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [HexColor("#fff3f3"), white]),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING",  (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ]))
        elemanlar.append(ml_tablo)

    # ── Depremler ───────────────────────────────────
    elemanlar.append(Paragraph("Son Depremler", bolum_stil))
    dep_veri = [["Tarih", "Saat", "Buyukluk", "Derinlik", "Yer"]]
    for d in depremler[:8]:
        dep_veri.append([
            str(d.get("tarih", "")),
            str(d.get("saat", "")),
            f"M{d.get('buyukluk', '')}",
            f"{d.get('derinlik_km', '')} km",
            str(d.get("yer", ""))[:45],
        ])
    dep_tablo = Table(dep_veri, colWidths=[2.5*cm, 2.5*cm, 2*cm, 2.5*cm, 7.5*cm])
    dep_tablo.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), LACIVERT),
        ("TEXTCOLOR",   (0,0), (-1,0), white),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("GRID",        (0,0), (-1,-1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, ACIK_MAV]),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ]))
    elemanlar.append(dep_tablo)

    # ── Footer ──────────────────────────────────────
    elemanlar.append(Spacer(1, 0.5*cm))
    elemanlar.append(Paragraph(
        f"Bu rapor Kurumsal Veri Entegrasyon Platformu tarafindan otomatik olusturulmustur. "
        f"Gelistirici: Mehmet Kerem Akkus | kerem45akkus@gmail.com | github.com/keremakkuus",
        ParagraphStyle("footer", fontSize=8, textColor=GRI)
    ))

    doc.build(elemanlar)
    print(f"✅ PDF raporu olusturuldu: {dosya}")
    return dosya


if __name__ == "__main__":
    from toplayici import hava_durumu_cek, deprem_verisi_cek
    from temizleyici import hava_verisi_temizle, deprem_verisi_temizle
    from ml_analiz import anomali_tespit_ml
    from veri_kaynaklari import doviz_kurlari_cek, hava_kalitesi_cek

    print("=" * 50)
    print("PDF RAPOR URETİCİ CALISIYOR")
    print("=" * 50)

    hava          = hava_verisi_temizle(hava_durumu_cek())
    depremler     = deprem_verisi_temizle(deprem_verisi_cek())
    ml_anomaliler = anomali_tespit_ml(depremler)
    doviz         = doviz_kurlari_cek()
    hava_kalitesi = hava_kalitesi_cek()

    pdf_rapor_olustur(hava, depremler, ml_anomaliler, doviz, hava_kalitesi)