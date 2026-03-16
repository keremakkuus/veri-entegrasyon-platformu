from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
auth = Blueprint("auth", __name__)

# ── Kullanıcılar (gerçek projede veritabanından gelir) ──
KULLANICILAR = {
    "admin": {
        "id": "1",
        "sifre": generate_password_hash("admin123"),
        "ad": "Mehmet Kerem Akkuş",
        "rol": "admin"
    },
    "izleyici": {
        "id": "2",
        "sifre": generate_password_hash("izleyici123"),
        "ad": "İzleyici Kullanıcı",
        "rol": "izleyici"
    }
}

class Kullanici(UserMixin):
    def __init__(self, id, kullanici_adi, ad, rol):
        self.id            = id
        self.kullanici_adi = kullanici_adi
        self.ad            = ad
        self.rol           = rol

@login_manager.user_loader
def kullanici_yukle(user_id):
    for kullanici_adi, bilgi in KULLANICILAR.items():
        if bilgi["id"] == user_id:
            return Kullanici(bilgi["id"], kullanici_adi, bilgi["ad"], bilgi["rol"])
    return None

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi")
        sifre         = request.form.get("sifre")

        if kullanici_adi in KULLANICILAR:
            bilgi = KULLANICILAR[kullanici_adi]
            if check_password_hash(bilgi["sifre"], sifre):
                kullanici = Kullanici(bilgi["id"], kullanici_adi, bilgi["ad"], bilgi["rol"])
                login_user(kullanici)
                return redirect(url_for("dashboard"))

        flash("Kullanıcı adı veya şifre hatalı!", "hata")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))