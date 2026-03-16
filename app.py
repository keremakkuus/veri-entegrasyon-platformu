from flask import Flask, render_template, jsonify, send_file, redirect, url_for
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading
import time
import os

from auth import auth, login_manager
from toplayici import hava_durumu_cek, deprem_verisi_cek
from temizleyici import hava_verisi_temizle, deprem_verisi_temizle
from ml_analiz import anomali_tespit_ml
from veritabani import veritabani_olustur, hava_kaydet, depremler_kaydet, istatistik_getir
from veri_kaynaklari import doviz_kurlari_cek, hava_kalitesi_cek
from pdf_rapor import pdf_rapor_olustur

app = Flask(__name__)
app.secret_key = "koski_veri_platformu_2026_gizli_anahtar"
socketio = SocketIO(app, cors_allowed_origins="*")

login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Lütfen önce giriş yapın!"

app.register_blueprint(auth)
veritabani_olustur()

# ── Önbellek ──────────────────────────────────────
son_veri = {}

def veri_guncelle():
    """Arka planda veri günceller ve WebSocket ile yayınlar"""
    global son_veri
    while True:
        try:
            hava      = hava_verisi_temizle(hava_durumu_cek())
            depremler = deprem_verisi_temizle(deprem_verisi_cek())
            ml        = anomali_tespit_ml(depremler)
            doviz     = doviz_kurlari_cek()
            kalite    = hava_kalitesi_cek()
            stats     = istatistik_getir()

            if hava:     hava_kaydet(hava)
            if depremler: depremler_kaydet(depremler)

            son_veri = {
                "hava"          : hava,
                "depremler"     : depremler,
                "ml_anomaliler" : ml,
                "doviz"         : doviz,
                "hava_kalitesi" : kalite,
                "istatistikler" : {
                    "toplam_hava"    : stats["toplam_hava"],
                    "toplam_deprem"  : stats["toplam_deprem"],
                    "toplam_anomali" : stats["toplam_anomali"],
                },
                "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            }

            # WebSocket ile tüm bağlı kullanıcılara gönder
            socketio.emit("veri_guncellendi", son_veri)
            print(f"✅ Veri güncellendi: {son_veri['guncelleme']}")

        except Exception as e:
            print(f"❌ Güncelleme hatası: {e}")

        time.sleep(300)  # 5 dakikada bir güncelle

# ── Rotalar ───────────────────────────────────────

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html", kullanici=current_user)

@app.route("/api/veri")
@login_required
def veri_getir():
    if not son_veri:
        # İlk yükleme
        hava      = hava_verisi_temizle(hava_durumu_cek())
        depremler = deprem_verisi_temizle(deprem_verisi_cek())
        ml        = anomali_tespit_ml(depremler)
        doviz     = doviz_kurlari_cek()
        kalite    = hava_kalitesi_cek()
        stats     = istatistik_getir()
        return jsonify({
            "hava": hava, "depremler": depremler,
            "ml_anomaliler": ml, "doviz": doviz,
            "hava_kalitesi": kalite,
            "istatistikler": {
                "toplam_hava": stats["toplam_hava"],
                "toplam_deprem": stats["toplam_deprem"],
                "toplam_anomali": stats["toplam_anomali"],
            },
            "guncelleme": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        })
    return jsonify(son_veri)

@app.route("/api/pdf")
@login_required
def pdf_indir():
    try:
        if son_veri:
            dosya = pdf_rapor_olustur(
                son_veri["hava"],
                son_veri["depremler"],
                son_veri["ml_anomaliler"],
                son_veri["doviz"],
                son_veri["hava_kalitesi"]
            )
            return send_file(dosya, as_attachment=True)
        return jsonify({"hata": "Veri henüz yüklenmedi"}), 400
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

# ── WebSocket ─────────────────────────────────────

@socketio.on("connect")
def baglan():
    print(f"✅ Kullanıcı bağlandı")
    if son_veri:
        emit("veri_guncellendi", son_veri)

if __name__ == "__main__":
    print("=" * 55)
    print("  KURUMSAL VERİ PLATFORMU v2.0")
    print("  http://localhost:5000")
    print("  Admin: admin / admin123")
    print("=" * 55)

    # Arka plan veri güncelleme thread'i
    t = threading.Thread(target=veri_guncelle, daemon=True)
    t.start()

    socketio.run(app, debug=False, port=5000, allow_unsafe_werkzeug=True)
