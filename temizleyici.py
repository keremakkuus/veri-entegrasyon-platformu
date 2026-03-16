import pandas as pd
from datetime import datetime
import logging

def hava_verisi_temizle(veri):
    """Hava durumu verisini temizler ve düzenler"""
    if veri is None:
        return None

    try:
        temiz = {
            "kaynak": str(veri.get("kaynak", "Bilinmiyor")),
            "sehir": str(veri.get("sehir", "Bilinmiyor")),
            "sicaklik_C": float(veri.get("sicaklik_C", 0)),
            "nem_%": float(veri.get("nem_%", 0)),
            "hissedilen_C": float(veri.get("hissedilen_C", 0)),
            "durum": str(veri.get("durum", "Bilinmiyor")),
            "zaman": veri.get("zaman", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        logging.info("Hava verisi temizlendi")
        print(f"✅ Hava verisi temizlendi: {temiz['sicaklik_C']}°C, Nem: {temiz['nem_%']}%")
        return temiz

    except Exception as e:
        logging.error(f"Hava verisi temizleme hatası: {e}")
        print(f"❌ Temizleme hatası: {e}")
        return None


def deprem_verisi_temizle(depremler):
    """Deprem verilerini temizler ve filtreler"""
    if not depremler:
        return []

    try:
        temiz_liste = []
        for d in depremler:
            try:
                buyukluk = float(d.get("buyukluk", 0))
                derinlik = float(d.get("derinlik", 0))

                temiz = {
                    "tarih": str(d.get("tarih", "")),
                    "saat": str(d.get("saat", "")),
                    "enlem": float(d.get("enlem", 0)),
                    "boylam": float(d.get("boylam", 0)),
                    "derinlik_km": derinlik,
                    "buyukluk": buyukluk,
                    "yer": str(d.get("yer", "Bilinmiyor")),
                    "tehlike_seviyesi": tehlike_hesapla(buyukluk),
                    "zaman": d.get("zaman", "")
                }
                temiz_liste.append(temiz)

            except Exception:
                continue  # Hatalı satırı atla

        logging.info(f"{len(temiz_liste)} deprem verisi temizlendi")
        print(f"✅ {len(temiz_liste)} deprem verisi temizlendi")
        return temiz_liste

    except Exception as e:
        logging.error(f"Deprem temizleme hatası: {e}")
        print(f"❌ Hata: {e}")
        return []


def tehlike_hesapla(buyukluk):
    """Deprem büyüklüğüne göre tehlike seviyesi belirler"""
    if buyukluk >= 6.0:
        return "🔴 YÜKSEK"
    elif buyukluk >= 4.0:
        return "🟠 ORTA"
    elif buyukluk >= 2.0:
        return "🟡 DÜŞÜK"
    else:
        return "🟢 ÇOKMINÖR"


if __name__ == "__main__":
    # Test için örnek veri
    from toplayici import hava_durumu_cek, deprem_verisi_cek

    print("=" * 40)
    print("VERİ TEMİZLEYİCİ ÇALIŞIYOR")
    print("=" * 40)

    hava = hava_durumu_cek()
    temiz_hava = hava_verisi_temizle(hava)

    depremler = deprem_verisi_cek()
    temiz_depremler = deprem_verisi_temizle(depremler)

    if temiz_depremler:
        print("\n📋 Temizlenmiş Deprem Verileri:")
        for d in temiz_depremler[:3]:
            print(f"  → {d['tarih']} {d['saat']} | M{d['buyukluk']} | {d['yer']} | {d['tehlike_seviyesi']}")


