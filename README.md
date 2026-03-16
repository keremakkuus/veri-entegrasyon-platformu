# 🏢 Kurumsal Veri Entegrasyon Platformu

Farklı kaynaklardan otomatik veri toplayan, temizleyen ve Excel raporu üreten kurumsal otomasyon sistemi.

## 🚀 Özellikler

- 📡 **Gerçek zamanlı veri toplama** — Hava durumu ve deprem verisi (Kandilli Rasathanesi)
- 🧹 **Otomatik veri temizleme** — Doğrulama, tip kontrolü ve hata ayıklama
- 📊 **Excel rapor üretimi** — 3 sayfalı otomatik rapor (Özet, Hava, Depremler)
- ⏰ **Zamanlayıcı sistemi** — Saatte bir otomatik çalışma
- 📝 **Loglama** — Tüm işlemler kayıt altında
- ⚠️ **Tehlike seviyesi hesaplama** — Deprem büyüklüğüne göre otomatik sınıflandırma

## 🗂️ Proje Yapısı
```
veri_platformu/
├── main.py           → Ana çalıştırıcı ve zamanlayıcı
├── toplayici.py      → Veri çekme modülü
├── temizleyici.py    → Veri temizleme ve doğrulama
├── raporlayici.py    → Excel rapor üretici
└── logs/             → İşlem kayıtları
```

## ⚙️ Kurulum
```bash
pip install requests beautifulsoup4 schedule pandas openpyxl
```

## ▶️ Çalıştırma
```bash
py main.py
```

## 📋 Örnek Çıktı
```
╔══════════════════════════════════════════╗
║   KURUMSAL VERİ ENTEGRASYON PLATFORMU   ║
║        v1.0 — Mehmet Kerem Akkuş        ║
╚══════════════════════════════════════════╝

✅ PIPELINE TAMAMLANDI!
   🌤  Sıcaklık   : 4.0°C - Partly cloudy
   💧 Nem         : 60.0%
   🌍 Deprem      : 10 adet
   📁 Rapor       : raporlar/rapor_20260316.xlsx
```

## 🛠️ Kullanılan Teknolojiler

- **Python 3.14**
- **requests** — HTTP istekleri
- **BeautifulSoup4** — Web scraping
- **pandas** — Veri işleme
- **openpyxl** — Excel üretimi
- **schedule** — Zamanlayıcı

## 👤 Geliştirici

**Mehmet Kerem Akkuş** — Yazılım Mühendisi  
📧 kerem45akkus@gmail.com
