import pandas as pd
import os
from datetime import datetime
import logging

os.makedirs("raporlar", exist_ok=True)

def rapor_olustur(hava_verisi, deprem_listesi):
    """Excel raporu oluşturur"""
    try:
        dosya_adi = f"raporlar/rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        with pd.ExcelWriter(dosya_adi, engine="openpyxl") as writer:

            # ── Hava Durumu Sayfası ──
            if hava_verisi:
                hava_df = pd.DataFrame([hava_verisi])
                hava_df.to_excel(writer, sheet_name="Hava Durumu", index=False)
                print("✅ Hava durumu sayfası oluşturuldu")

            # ── Deprem Verileri Sayfası ──
            if deprem_listesi:
                deprem_df = pd.DataFrame(deprem_listesi)
                deprem_df.to_excel(writer, sheet_name="Depremler", index=False)
                print(f"✅ Deprem sayfası oluşturuldu ({len(deprem_listesi)} kayıt)")

            # ── Özet Sayfası ──
            ozet_data = {
                "Bilgi": [
                    "Rapor Tarihi",
                    "Konya Sıcaklık",
                    "Konya Nem",
                    "Hava Durumu",
                    "Toplam Deprem",
                    "En Büyük Deprem",
                    "Tehlikeli Deprem (M4+)",
                ],
                "Değer": [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    f"{hava_verisi['sicaklik_C']}°C" if hava_verisi else "-",
                    f"{hava_verisi['nem_%']}%" if hava_verisi else "-",
                    hava_verisi['durum'] if hava_verisi else "-",
                    len(deprem_listesi),
                    max([d['buyukluk'] for d in deprem_listesi]) if deprem_listesi else "-",
                    len([d for d in deprem_listesi if d['buyukluk'] >= 4.0]),
                ]
            }
            ozet_df = pd.DataFrame(ozet_data)
            ozet_df.to_excel(writer, sheet_name="Özet", index=False)
            print("✅ Özet sayfası oluşturuldu")

        logging.info(f"Rapor oluşturuldu: {dosya_adi}")
        print(f"\n📁 Rapor kaydedildi: {dosya_adi}")
        return dosya_adi

    except Exception as e:
        logging.error(f"Rapor hatası: {e}")
        print(f"❌ Rapor hatası: {e}")
        return None


if __name__ == "__main__":
    from toplayici import hava_durumu_cek, deprem_verisi_cek
    from temizleyici import hava_verisi_temizle, deprem_verisi_temizle

    print("=" * 40)
    print("RAPORLAYICI ÇALIŞIYOR")
    print("=" * 40)

    hava = hava_verisi_temizle(hava_durumu_cek())
    depremler = deprem_verisi_temizle(deprem_verisi_cek())

    rapor_olustur(hava, depremler)