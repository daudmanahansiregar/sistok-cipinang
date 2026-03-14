from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Mengatur lokasi database agar aman
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pesan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    isi_pesan = db.Column(db.String(500), nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)

# Membuat database dan folder instance otomatis
if not os.path.exists('instance'):
    os.makedirs('instance')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Waduh! File index.html nggak ketemu di folder templates. Error: {e}"

@app.route('/simpan', methods=['POST'])
def simpan():
    nama = request.form.get('nama')
    teks = request.form.get('pesan')
    if nama and teks:
        baru = Pesan(nama=nama, isi_pesan=teks)
        db.session.add(baru)
        db.session.commit()
    return "OK"

@app.route('/admin-panel')
def admin():
    semua_pesan = Pesan.query.order_by(Pesan.tanggal.desc()).all()
    return render_template('admin.html', pesan=semua_pesan)

if __name__ == '__main__':
    print("--- MENCOBA MENYALAKAN MESIN ---")
    app.run(debug=True, port=5000)