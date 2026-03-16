import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime

def anomali_tespit_ml(depremler):
    """
    Makine öğrenmesi ile deprem verilerinde anomali tespiti.
    Isolation Forest algoritması kullanır.
    """
    if len(depremler) < 5:
        print("⚠️ Yeterli veri yok, ML analizi atlandı")
        return []

    try:
        # Özellik matrisi oluştur
        X = np.array([
            [float(d.get("buyukluk", 0)),
             float(d.get("derinlik_km", 0)),
             float(d.get("enlem", 0)),
             float(d.get("boylam", 0))]
            for d in depremler
        ])

        # Veriyi ölçeklendir
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Isolation Forest modeli
        model = IsolationForest(
            contamination=0.2,  # %20 anomali beklentisi
            random_state=42,
            n_estimators=100
        )
        tahminler = model.fit_predict(X_scaled)
        skorlar   = model.score_samples(X_scaled)

        # Anomali olanları işaretle
        anomaliler = []
        for i, (deprem, tahmin, skor) in enumerate(zip(depremler, tahminler, skorlar)):
            if tahmin == -1:  # -1 = anomali
                anomaliler.append({
                    "index"    : i,
                    "yer"      : deprem.get("yer", "Bilinmiyor"),
                    "buyukluk" : deprem.get("buyukluk", 0),
                    "derinlik" : deprem.get("derinlik_km", 0),
                    "skor"     : round(float(skor), 4),
                    "aciklama" : anomali_acikla(deprem, skor),
                })

        print(f"✅ ML Analizi tamamlandı: {len(anomaliler)} anomali tespit edildi")
        return anomaliler

    except Exception as e:
        print(f"❌ ML analiz hatası: {e}")
        return []


def anomali_acikla(deprem, skor):
    """Anomalinin neden tespit edildiğini açıklar"""
    buyukluk  = float(deprem.get("buyukluk", 0))
    derinlik  = float(deprem.get("derinlik_km", 0))
    aciklamalar = []

    if buyukluk >= 4.0:
        aciklamalar.append(f"Yüksek büyüklük (M{buyukluk})")
    if derinlik < 5:
        aciklamalar.append(f"Çok sığ deprem ({derinlik} km)")
    if derinlik > 100:
        aciklamalar.append(f"Çok derin deprem ({derinlik} km)")
    if skor < -0.15:
        aciklamalar.append("İstatistiksel aykırı değer")

    return " | ".join(aciklamalar) if aciklamalar else "Genel anomali"


def hava_trend_analizi(hava_gecmis):
    """Hava durumu trend analizi yapar"""
    if len(hava_gecmis) < 3:
        return {"durum": "Yetersiz veri"}

    try:
        sicakliklar = [float(h.get("sicaklik_C", 0)) for h in hava_gecmis]
        nemler      = [float(h.get("nem_%", 0)) for h in hava_gecmis]

        # Trend hesapla
        sicaklik_trend = "artıyor 📈" if sicakliklar[-1] > sicakliklar[0] else "azalıyor 📉"
        nem_trend      = "artıyor 📈" if nemler[-1] > nemler[0] else "azalıyor 📉"

        return {
            "sicaklik_ort"   : round(np.mean(sicakliklar), 1),
            "sicaklik_min"   : round(np.min(sicakliklar), 1),
            "sicaklik_max"   : round(np.max(sicakliklar), 1),
            "sicaklik_trend" : sicaklik_trend,
            "nem_ort"        : round(np.mean(nemler), 1),
            "nem_trend"      : nem_trend,
            "olcum_sayisi"   : len(hava_gecmis),
        }
    except Exception as e:
        return {"durum": f"Hata: {e}"}


if __name__ == "__main__":
    from toplayici import hava_durumu_cek, deprem_verisi_cek
    from temizleyici import hava_verisi_temizle, deprem_verisi_temizle

    print("=" * 50)
    print("ML ANALİZ MODÜLü ÇALIŞIYOR")
    print("=" * 50)

    # Deprem ML analizi
    depremler = deprem_verisi_temizle(deprem_verisi_cek())
    anomaliler = anomali_tespit_ml(depremler)

    if anomaliler:
        print("\n🤖 ML ile Tespit Edilen Anomaliler:")
        for a in anomaliler:
            print(f"  → {a['yer']}")
            print(f"     Büyüklük: M{a['buyukluk']} | Derinlik: {a['derinlik']} km")
            print(f"     Açıklama: {a['aciklama']}")
            print(f"     Anomali Skoru: {a['skor']}")
            print()

    # Hava trend analizi
    print("\n📊 Hava Durumu Trend Analizi:")
    hava_listesi = []
    for _ in range(5):
        h = hava_verisi_temizle(hava_durumu_cek())
        if h:
            hava_listesi.append(h)

    trend = hava_trend_analizi(hava_listesi)
    for k, v in trend.items():
        print(f"   {k}: {v}")