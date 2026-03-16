import requests
from datetime import datetime
import logging

def doviz_kurlari_cek():
    """Güncel döviz kurlarını çeker"""
    try:
        url = "https://api.exchangerate-api.com/v4/latest/TRY"
        yanit = requests.get(url, timeout=10)
        yanit.raise_for_status()
        veri = yanit.json()

        kurlar = {
            "USD_TRY": round(1 / veri["rates"].get("USD", 1), 2),
            "EUR_TRY": round(1 / veri["rates"].get("EUR", 1), 2),
            "GBP_TRY": round(1 / veri["rates"].get("GBP", 1), 2),
            "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"✅ Döviz kurları çekildi: 1 USD = {kurlar['USD_TRY']} TL")
        return kurlar

    except Exception as e:
        print(f"❌ Döviz hatası: {e}")
        return {"USD_TRY": 0, "EUR_TRY": 0, "GBP_TRY": 0, "zaman": "-"}


def hava_kalitesi_cek():
    """Konya hava kalitesi verisi çeker"""
    try:
        # Open-Meteo ücretsiz API (kayıt gerektirmez)
        url = (
            "https://air-quality-api.open-meteo.com/v1/air-quality"
            "?latitude=37.87&longitude=32.49"
            "&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone"
            "&forecast_days=1"
        )
        yanit = requests.get(url, timeout=10)
        yanit.raise_for_status()
        veri = yanit.json()

        # En son saatin verisi
        pm10  = veri["hourly"]["pm10"][-1]
        pm25  = veri["hourly"]["pm2_5"][-1]
        co    = veri["hourly"]["carbon_monoxide"][-1]
        no2   = veri["hourly"]["nitrogen_dioxide"][-1]
        ozon  = veri["hourly"]["ozone"][-1]

        kalite = hava_kalite_indeksi(pm10, pm25)

        sonuc = {
            "pm10"  : round(pm10, 1),
            "pm2_5" : round(pm25, 1),
            "co"    : round(co, 1),
            "no2"   : round(no2, 1),
            "ozon"  : round(ozon, 1),
            "kalite": kalite,
            "zaman" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"✅ Hava kalitesi çekildi: PM10={pm10}, Kalite={kalite}")
        return sonuc

    except Exception as e:
        print(f"❌ Hava kalitesi hatası: {e}")
        return {"pm10": 0, "pm2_5": 0, "co": 0, "no2": 0, "ozon": 0, "kalite": "Bilinmiyor", "zaman": "-"}


def hava_kalite_indeksi(pm10, pm25):
    """PM değerlerine göre hava kalite indeksi"""
    if pm10 <= 20 and pm25 <= 10:
        return "🟢 İyi"
    elif pm10 <= 40 and pm25 <= 20:
        return "🟡 Orta"
    elif pm10 <= 50 and pm25 <= 25:
        return "🟠 Hassas"
    elif pm10 <= 100 and pm25 <= 50:
        return "🔴 Sağlıksız"
    else:
        return "🟣 Tehlikeli"


if __name__ == "__main__":
    print("=" * 50)
    print("VERİ KAYNAKLARI TEST EDİLİYOR")
    print("=" * 50)

    print("\n💱 Döviz Kurları:")
    doviz = doviz_kurlari_cek()
    for k, v in doviz.items():
        if k != "zaman":
            print(f"   {k}: {v} TL")

    print("\n🌿 Hava Kalitesi (Konya):")
    kalite = hava_kalitesi_cek()
    for k, v in kalite.items():
        print(f"   {k}: {v}")