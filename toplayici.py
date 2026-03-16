import requests
from bs4 import BeautifulSoup
import logging
import os
from datetime import datetime

# Log klasörünü oluştur
os.makedirs("logs", exist_ok=True)

# Loglama ayarları
logging.basicConfig(
    filename=f"logs/log_{datetime.now().strftime('%Y%m%d')}.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def hava_durumu_cek():
    """Konya hava durumu verisi çeker"""
    try:
        url = "https://wttr.in/Konya?format=j1"
        yanit = requests.get(url, timeout=10)
        yanit.raise_for_status()
        veri = yanit.json()

        sicaklik = veri["current_condition"][0]["temp_C"]
        nem = veri["current_condition"][0]["humidity"]
        hissedilen = veri["current_condition"][0]["FeelsLikeC"]
        durum = veri["current_condition"][0]["weatherDesc"][0]["value"]

        sonuc = {
            "kaynak": "Hava Durumu",
            "sehir": "Konya",
            "sicaklik_C": sicaklik,
            "nem_%": nem,
            "hissedilen_C": hissedilen,
            "durum": durum,
            "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        logging.info(f"Hava durumu verisi başarıyla çekildi: {sicaklik}°C")
        print(f"✅ Hava durumu çekildi: {sicaklik}°C, {durum}")
        return sonuc

    except Exception as e:
        logging.error(f"Hava durumu hatası: {e}")
        print(f"❌ Hata: {e}")
        return None


def deprem_verisi_cek():
    """Kandilli Rasathanesi'nden son depremleri çeker"""
    try:
        url = "http://www.koeri.boun.edu.tr/scripts/lst0.asp"
        headers = {"User-Agent": "Mozilla/5.0"}
        yanit = requests.get(url, headers=headers, timeout=10)
        yanit.encoding = "windows-1254"
        soup = BeautifulSoup(yanit.text, "html.parser")

        pre = soup.find("pre")
        satirlar = pre.text.strip().split("\n")[6:16]  # İlk 10 deprem

        depremler = []
        for satir in satirlar:
            parcalar = satir.split()
            if len(parcalar) >= 6:
                depremler.append({
                    "tarih": parcalar[0],
                    "saat": parcalar[1],
                    "enlem": parcalar[2],
                    "boylam": parcalar[3],
                    "derinlik": parcalar[4],
                    "buyukluk": parcalar[6],
                    "yer": " ".join(parcalar[8:]),
                    "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        logging.info(f"{len(depremler)} deprem verisi çekildi")
        print(f"✅ {len(depremler)} deprem verisi çekildi")
        return depremler

    except Exception as e:
        logging.error(f"Deprem verisi hatası: {e}")
        print(f"❌ Hata: {e}")
        return []


if __name__ == "__main__":
    print("=" * 40)
    print("VERİ TOPLAYICI ÇALIŞIYOR")
    print("=" * 40)
    hava_durumu_cek()
    deprem_verisi_cek()

