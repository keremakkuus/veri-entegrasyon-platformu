from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

os.makedirs("db", exist_ok=True)

engine = create_engine("sqlite:///db/veri_platformu.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# ── Tablolar ──────────────────────────────────────────

class HavaDurumu(Base):
    __tablename__ = "hava_durumu"
    id           = Column(Integer, primary_key=True)
    sehir        = Column(String(50))
    sicaklik_C   = Column(Float)
    nem          = Column(Float)
    hissedilen_C = Column(Float)
    durum        = Column(String(100))
    kayit_zamani = Column(DateTime, default=datetime.now)

class Deprem(Base):
    __tablename__ = "depremler"
    id           = Column(Integer, primary_key=True)
    tarih        = Column(String(20))
    saat         = Column(String(20))
    enlem        = Column(Float)
    boylam       = Column(Float)
    derinlik_km  = Column(Float)
    buyukluk     = Column(Float)
    yer          = Column(String(200))
    tehlike      = Column(String(50))
    kayit_zamani = Column(DateTime, default=datetime.now)

class Anomali(Base):
    __tablename__ = "anomaliler"
    id           = Column(Integer, primary_key=True)
    kaynak       = Column(String(50))
    parametre    = Column(String(50))
    deger        = Column(Float)
    esik         = Column(Float)
    aciklama     = Column(Text)
    seviye       = Column(String(20))
    kayit_zamani = Column(DateTime, default=datetime.now)

class PipelineLog(Base):
    __tablename__ = "pipeline_log"
    id             = Column(Integer, primary_key=True)
    baslangic      = Column(DateTime)
    bitis          = Column(DateTime)
    durum          = Column(String(20))
    deprem_sayisi  = Column(Integer)
    anomali_sayisi = Column(Integer)
    notlar         = Column(Text)

def veritabani_olustur():
    Base.metadata.create_all(engine)
    print("✅ Veritabanı oluşturuldu: db/veri_platformu.db")

def hava_kaydet(veri):
    session = Session()
    try:
        kayit = HavaDurumu(
            sehir        = veri.get("sehir", ""),
            sicaklik_C   = float(veri.get("sicaklik_C", 0)),
            nem          = float(veri.get("nem_%", 0)),
            hissedilen_C = float(veri.get("hissedilen_C", 0)),
            durum        = veri.get("durum", ""),
        )
        session.add(kayit)
        session.commit()
        print("✅ Hava durumu veritabanına kaydedildi")
    except Exception as e:
        session.rollback()
        print(f"❌ Hava kayıt hatası: {e}")
    finally:
        session.close()

def depremler_kaydet(depremler):
    session = Session()
    try:
        for d in depremler:
            kayit = Deprem(
                tarih       = d.get("tarih", ""),
                saat        = d.get("saat", ""),
                enlem       = float(d.get("enlem", 0)),
                boylam      = float(d.get("boylam", 0)),
                derinlik_km = float(d.get("derinlik_km", 0)),
                buyukluk    = float(d.get("buyukluk", 0)),
                yer         = d.get("yer", ""),
                tehlike     = d.get("tehlike_seviyesi", ""),
            )
            session.add(kayit)
        session.commit()
        print(f"✅ {len(depremler)} deprem veritabanına kaydedildi")
    except Exception as e:
        session.rollback()
        print(f"❌ Deprem kayıt hatası: {e}")
    finally:
        session.close()

def anomali_kaydet(kaynak, parametre, deger, esik, aciklama, seviye):
    session = Session()
    try:
        kayit = Anomali(
            kaynak     = kaynak,
            parametre  = parametre,
            deger      = deger,
            esik       = esik,
            aciklama   = aciklama,
            seviye     = seviye,
        )
        session.add(kayit)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def istatistik_getir():
    session = Session()
    try:
        return {
            "toplam_hava"    : session.query(HavaDurumu).count(),
            "toplam_deprem"  : session.query(Deprem).count(),
            "toplam_anomali" : session.query(Anomali).count(),
            "toplam_pipeline": session.query(PipelineLog).count(),
            "son_depremler"  : session.query(Deprem).order_by(Deprem.id.desc()).limit(5).all(),
            "son_anomaliler" : session.query(Anomali).order_by(Anomali.id.desc()).limit(5).all(),
        }
    finally:
        session.close()

if __name__ == "__main__":
    veritabani_olustur()
    print("Tablolar: hava_durumu, depremler, anomaliler, pipeline_log")