import schedule
import time
import logging
import os
from datetime import datetime

from toplayici import hava_durumu_cek, deprem_verisi_cek
from temizleyici import hava_verisi_temizle, deprem_verisi_temizle
from raporlayici import rapor_olustur

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=f"logs/log_{datetime.now().strftime('%Y%m%d')}.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def pipeline_calistir():
    """Tüm veri toplama sürecini çalıştırır"""
    print("\n" + "=" * 50)
    print(f"🚀 PIPELINE BAŞLADI: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 1. Veri Toplama
    print("\n📡 ADIM 1: Veri Toplanıyor...")
    hava = hava_durumu_cek()
    depremler = deprem_verisi_cek()

    # 2. Veri Temizleme
    print("\n🧹 ADIM 2: Veri Temizleniyor...")
    temiz_hava = hava_verisi_temizle(hava)
    temiz_depremler = deprem_verisi_temizle(depremler)

    # 3. Raporlama
    print("\n📊 ADIM 3: Rapor Oluşturuluyor...")
    rapor_dosyasi = rapor_olustur(temiz_hava, temiz_depremler)

    # 4. Özet
    print("\n" + "=" * 50)
    print("✅ PIPELINE TAMAMLANDI!")
    print(f"   🌤  Sıcaklık   : {temiz_hava['sicaklik_C']}°C - {temiz_hava['durum']}")
    print(f"   💧 Nem         : {temiz_hava['nem_%']}%")
    print(f"   🌍 Deprem      : {len(temiz_depremler)} adet")
    tehlikeli = [d for d in temiz_depremler if d['buyukluk'] >= 4.0]
    if tehlikeli:
        print(f"   ⚠️  Tehlikeli   : {len(tehlikeli)} adet (M4.0+)")
    print(f"   📁 Rapor       : {rapor_dosyasi}")
    print("=" * 50)

    logging.info("Pipeline başarıyla tamamlandı")


# ── Zamanlayıcı: Her saat başı çalışır ──
schedule.every().hour.do(pipeline_calistir)

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   KURUMSAL VERİ ENTEGRASYON PLATFORMU   ║")
    print("║        v1.0 — Mehmet Kerem Akkuş        ║")
    print("╚══════════════════════════════════════════╝")
    print("\n⏰ Sistem her saat otomatik çalışacak")
    print("   Şimdi ilk çalıştırma yapılıyor...\n")

    # İlk çalıştırma hemen
    pipeline_calistir()

    # Sonraki çalıştırmalar zamanlanmış
    print("\n⏳ Sistem beklemede... (durdurmak için Ctrl+C)")
    while True:
        schedule.run_pending()
        time.sleep(60)