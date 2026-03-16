from flask import Flask, render_template, jsonify
from datetime import datetime
from toplayici import hava_durumu_cek, deprem_verisi_cek
from temizleyici import hava_verisi_temizle, deprem_verisi_temizle
from ml_analiz import anomali_tespit_ml
from veritabani import veritabani_olustur, hava_kaydet, depremler_kaydet, istatistik_getir
import os

app = Flask(__name__)
veritabani_olustur()

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/veri")
def veri_getir():
    try:
        hava      = hava_verisi_temizle(hava_durumu_cek())
        depremler = deprem_verisi_temizle(deprem_verisi_cek())
        ml        = anomali_tespit_ml(depremler)

        if hava:
            hava_kaydet(hava)
        if depremler:
            depremler_kaydet(depremler)

        stats = istatistik_getir()

        return jsonify({
            "hava"           : hava,
            "depremler"      : depremler,
            "ml_anomaliler"  : ml,
            "istatistikler"  : {
                "toplam_hava"    : stats["toplam_hava"],
                "toplam_deprem"  : stats["toplam_deprem"],
                "toplam_anomali" : stats["toplam_anomali"],
            },
            "guncelleme"     : datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        })
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == "__main__":
    print("=" * 50)
    print("  KURUMSAL VERİ PLATFORMU — WEB DASHBOARD")
    print("  http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
