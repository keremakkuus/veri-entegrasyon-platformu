import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# ── E-posta Ayarları ──────────────────────────────────
# Gmail kullanıyorsanız "Uygulama Şifresi" gerekir
# Google Hesabı → Güvenlik → 2 Adımlı Doğrulama → Uygulama Şifreleri
GONDEREN  = "kerem45akkus@gmail.com"
SIFRE     = "uxpcgjitczpaebei"  # Gmail uygulama şifresi
ALICI     = "kerem45akkus@gmail.com"

def email_gonder(konu, icerik_html):
    """HTML formatlı e-posta gönderir"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = konu
        msg["From"]    = GONDEREN
        msg["To"]      = ALICI

        html_part = MIMEText(icerik_html, "html", "utf-8")
        msg.attach(html_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GONDEREN, SIFRE)
            server.sendmail(GONDEREN, ALICI, msg.as_string())

        print(f"✅ E-posta gönderildi: {konu}")
        return True

    except Exception as e:
        print(f"❌ E-posta gönderilemedi: {e}")
        print("   (Gmail uygulama şifresi gerekli)")
        return False


def anomali_email_olustur(hava, depremler, ml_anomaliler):
    """Anomali uyarı e-postası oluşturur"""

    buyuk_depremler = [d for d in depremler if float(d.get("buyukluk", 0)) >= 3.0]
    kritik_depremler = [d for d in depremler if float(d.get("buyukluk", 0)) >= 4.0]

    html = f"""
    <html><body style="font-family: Arial; max-width: 700px; margin: auto;">

    <div style="background: #0D2149; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
        <h2 style="margin:0;">🏢 Kurumsal Veri Entegrasyon Platformu</h2>
        <p style="margin:5px 0 0 0; opacity:0.8;">Otomatik Anomali Raporu — {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
    </div>

    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 0 0 8px 8px;">

        <!-- Hava Durumu -->
        <h3 style="color: #0D2149;">🌤 Konya Hava Durumu</h3>
        <table style="width:100%; border-collapse:collapse;">
            <tr style="background:#E8EEF8;">
                <td style="padding:8px; border:1px solid #ddd;"><b>Sıcaklık</b></td>
                <td style="padding:8px; border:1px solid #ddd;">{hava.get('sicaklik_C', '-')}°C</td>
                <td style="padding:8px; border:1px solid #ddd;"><b>Nem</b></td>
                <td style="padding:8px; border:1px solid #ddd;">%{hava.get('nem_%', '-')}</td>
            </tr>
            <tr>
                <td style="padding:8px; border:1px solid #ddd;"><b>Durum</b></td>
                <td style="padding:8px; border:1px solid #ddd;" colspan="3">{hava.get('durum', '-')}</td>
            </tr>
        </table>

        <!-- Deprem Özeti -->
        <h3 style="color: #0D2149;">🌍 Deprem Özeti</h3>
        <table style="width:100%; border-collapse:collapse;">
            <tr style="background:#E8EEF8;">
                <td style="padding:8px; border:1px solid #ddd;"><b>Toplam Deprem</b></td>
                <td style="padding:8px; border:1px solid #ddd;">{len(depremler)}</td>
            </tr>
            <tr>
                <td style="padding:8px; border:1px solid #ddd;"><b>M3.0+ Deprem</b></td>
                <td style="padding:8px; border:1px solid #ddd; color: {'red' if buyuk_depremler else 'green'};">
                    {len(buyuk_depremler)}
                </td>
            </tr>
            <tr style="background:#E8EEF8;">
                <td style="padding:8px; border:1px solid #ddd;"><b>M4.0+ Kritik</b></td>
                <td style="padding:8px; border:1px solid #ddd; color: {'red' if kritik_depremler else 'green'}; font-weight:bold;">
                    {len(kritik_depremler)}
                </td>
            </tr>
        </table>

        <!-- ML Anomaliler -->
        {"<h3 style='color:red;'>🤖 ML Anomali Tespiti</h3>" if ml_anomaliler else ""}
        {"".join([f"<div style='background:#fff3f3; border-left:4px solid red; padding:10px; margin:5px 0;'><b>{a['yer']}</b><br>M{a['buyukluk']} | {a['aciklama']}</div>" for a in ml_anomaliler]) if ml_anomaliler else ""}

        <!-- Son Depremler -->
        <h3 style="color: #0D2149;">📋 Son Depremler</h3>
        <table style="width:100%; border-collapse:collapse;">
            <tr style="background:#0D2149; color:white;">
                <th style="padding:8px;">Tarih/Saat</th>
                <th style="padding:8px;">Büyüklük</th>
                <th style="padding:8px;">Yer</th>
                <th style="padding:8px;">Tehlike</th>
            </tr>
            {"".join([f"<tr style='background:{'#fff3f3' if float(d.get('buyukluk',0))>=3 else 'white'}'><td style='padding:8px;border:1px solid #ddd;'>{d.get('tarih','')} {d.get('saat','')}</td><td style='padding:8px;border:1px solid #ddd;text-align:center;'><b>M{d.get('buyukluk','')}</b></td><td style='padding:8px;border:1px solid #ddd;'>{d.get('yer','')[:50]}</td><td style='padding:8px;border:1px solid #ddd;'>{d.get('tehlike_seviyesi','')}</td></tr>" for d in depremler[:5]])}
        </table>

        <p style="color:#888; font-size:12px; margin-top:20px; border-top:1px solid #eee; padding-top:10px;">
            Bu e-posta Kurumsal Veri Entegrasyon Platformu tarafından otomatik oluşturulmuştur.<br>
            Geliştirici: Mehmet Kerem Akkuş | kerem45akkus@gmail.com
        </p>
    </div>
    </body></html>
    """
    return html


def rapor_emaili_gonder(hava, depremler, ml_anomaliler):
    """Tam rapor e-postasını gönderir"""
    buyuk_deprem_var = any(float(d.get("buyukluk", 0)) >= 4.0 for d in depremler)
    ml_anomali_var   = len(ml_anomaliler) > 0

    if buyuk_deprem_var or ml_anomali_var:
        konu = f"⚠️ ANOMALİ UYARISI — {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    else:
        konu = f"✅ Günlük Rapor — {datetime.now().strftime('%d.%m.%Y %H:%M')}"

    html = anomali_email_olustur(hava, depremler, ml_anomaliler)
    return email_gonder(konu, html)


if __name__ == "__main__":
    from toplayici import hava_durumu_cek, deprem_verisi_cek
    from temizleyici import hava_verisi_temizle, deprem_verisi_temizle
    from ml_analiz import anomali_tespit_ml

    print("=" * 50)
    print("E-POSTA UYARI MODÜLü ÇALIŞIYOR")
    print("=" * 50)

    hava      = hava_verisi_temizle(hava_durumu_cek())
    depremler = deprem_verisi_temizle(deprem_verisi_cek())
    ml_anomali = anomali_tespit_ml(depremler)

    print("\n📧 E-posta gönderiliyor...")
    print("   (Gmail uygulama şifresi ayarlanmamışsa simüle edilir)\n")
    rapor_emaili_gonder(hava, depremler, ml_anomali)