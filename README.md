# ATK Dashboard - Sistem Manajemen Alat Tulis Kantor

Sistem monitoring dan manajemen stok ATK (Alat Tulis Kantor) berbasis web untuk Timbangan.

## 📋 Deskripsi

Aplikasi web untuk mengelola inventori ATK dengan fitur:
-  Manajemen item (CRUD)
-  Reservasi stok batch/bulk
-  Laporan penggunaan bulanan
-  Dashboard monitoring berdasarkan lokasi penyimpanan
-  Pencarian dan filter item
-  Responsive design

##  Fitur Utama

### 1. **Manajemen Inventori**
- Tambah item baru dengan MID, nama, stok, satuan, dan lokasi penyimpanan
- Edit informasi item
- Hapus item (beserta riwayat transaksi)
- Update stok (tambah/kurangi) dengan pencatatan tanggal

### 2. **Reservasi Stok**
- Reservasi batch: tambah stok beberapa item sekaligus dalam satu tanggal
- Autocomplete search untuk cepat menemukan item
- Validasi stok otomatis

### 3. **Laporan Bulanan**
- Laporan penggunaan dan reservasi per bulan
- Export ke CSV
- Detail transaksi setiap item

### 4. **Dashboard Monitoring**
- Pengelompokan item berdasarkan lokasi penyimpanan
- Status stok (Habis, Rendah, Sedang, Tinggi)
- Preview 5 item per lokasi dengan opsi "Lihat Semua"

### 5. **Pencarian & Filter**
- Search berdasarkan MID atau nama item
- Filter berdasarkan level stok
- Sorting (nama, stok, MID, lokasi)

##  Teknologi

**Backend:**
- Python 3.11+
- Flask 3.0.0
- Gunicorn 21.2.0 (Production WSGI Server)
- SQLite (database file, tidak perlu install server)

**Frontend:**
- HTML5
- CSS3 (Custom styling)
- Vanilla JavaScript (no framework)

## 📁 Struktur Project

```
atk-dashboard/
├── app.py                      # Backend Flask
├── atk.db                      # SQLite database (dibuat otomatis)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
│
├── start_production.sh         # 🚀 Production start (Linux)
├── stop_production.sh          # 🛑 Production stop (Linux)
├── status_production.sh        # 📊 Production status (Linux)
│
├── start_production.bat        # 🚀 Production start (Windows)
├── stop_production.bat         # 🛑 Production stop (Windows)
├── status_production.bat       # 📊 Production status (Windows)
│
│
└── app/
    ├── static/
    │   ├── css/
    │   │   └── style.css       # Styling aplikasi
    │   ├── images/
    │   │   └── logo.png        # Logo aplikasi
    │   └── js/
    │       ├── app.js          # JavaScript utama
    │       ├── dashboard.js    # JavaScript dashboard
    │       └── toast.js        # Sistem notifikasi
    └── templates/
        ├── index.html          # Halaman utama
        └── dashboard.html      # Halaman dashboard
```

##  Instalasi

### 🐧 Linux/Mac (RECOMMENDED)

**1. Install dependencies:**
```bash
cd atk-dashboard
pip install -r requirements.txt
```

**2. Jalankan production server:**
```bash
./start_production.sh
```

**3. Cek status:**
```bash
./status_production.sh
```

**4. Stop server:**
```bash
./stop_production.sh
```

**Akses aplikasi:**
- Local: http://127.0.0.1:5000
- Network: http://\[YOUR-IP\]:5000

---

### 💻 Windows Production

**1. Install dependencies:**
```cmd
cd atk-dashboard
pip install -r requirements.txt
```

**2. Jalankan production server:**
```cmd
start_production.bat
```

Output akan menampilkan:
```
========================================
  ATK Dashboard - Production Mode
========================================

[SUCCESS] Starting Gunicorn server...

========================================
  Server berhasil dijalankan!
========================================

[INFO] Informasi Server:
  - URL Lokal:    http://127.0.0.1:5000
  - URL Network:  http://localhost:5000
  - Workers:      4 processes

[INFO] Log Files:
  - Access Log:   access.log
  - Error Log:    error.log
```

**3. Cek status:**
```cmd
status_production.bat
```

**4. Stop server:**
```cmd
stop_production.bat
```

**Akses aplikasi:**
- Local: http://127.0.0.1:5000
- Network: http://\[YOUR-IP\]:5000

---

### Log Files (Production)

Setelah menjalankan production mode, akan dibuat 3 file log:

- **access.log** - Semua HTTP request
- **error.log** - Error dan exception
- **gunicorn.log** - Server startup/shutdown

**Lihat log real-time (Linux):**
```bash
tail -f access.log
tail -f error.log
```

**Lihat log real-time (Windows):**
```cmd
powershell Get-Content access.log -Wait
powershell Get-Content error.log -Wait
```

---

## 🐳 Docker Deployment

1. Build image:
```bash
docker build -t atk-dashboard .
```

2. Run container (Production mode):
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/atk.db:/app/atk.db \
  --name atk-app \
  atk-dashboard
```

3. Cek logs:
```bash
docker logs -f atk-app
```

4. Stop container:
```bash
docker stop atk-app
docker rm atk-app
```

---

## 📊 Database Schema

### Tabel `items`
```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mid TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    unit TEXT NOT NULL,
    storage_location TEXT DEFAULT ''
)
```

### Tabel `transactions`
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    type TEXT NOT NULL,           -- 'in' atau 'out'
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (item_id) REFERENCES items (id)
)
```

## 🔌 API Endpoints

### Items

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/items` | Ambil semua item |
| POST | `/api/items` | Tambah item baru |
| PUT | `/api/items/<id>` | Edit item |
| DELETE | `/api/items/<id>` | Hapus item |
| PUT | `/api/items/<id>/stock` | Update stok item |

### Bulk Operations

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/items/bulk_reservation` | Reservasi batch |

### Reports

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/reports/monthly?month=YYYY-MM` | Laporan bulanan |
| GET | `/api/reports/monthly/export?month=YYYY-MM` | Export CSV |

### Dashboard

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/dashboard/storage` | Data dashboard |

##  Cara Penggunaan

### 1. Tambah Item Baru
1. Buka tab "Inventori" → Sub-tab "Reservasi"
2. Isi form "Tambah Item Baru"
3. Klik "Tambah Item"

### 2. Reservasi Stok Batch
1. Tab "Inventori" → "Reservasi"
2. Pilih tanggal reservasi
3. Ketik MID/nama item di search box
4. Pilih item dari dropdown
5. Masukkan jumlah
6. Klik "Tambah Baris" untuk item selanjutnya
7. Klik "Simpan Semua Reservasi"

### 3. Update Stok Manual
1. Tab "Inventori" → "Stock"
2. Pada item card, klik:
   - "➕ Tambah Stok" untuk reservasi
   - "➖ Kurangi Stok" untuk penggunaan
3. Masukkan jumlah dan tanggal
4. Simpan

### 4. Lihat Laporan
1. Tab "Laporan Bulanan"
2. Pilih bulan
3. Klik "Lihat Laporan"
4. Klik "Export CSV" untuk download

### 5. Dashboard Monitoring
1. Klik "📊 Lihat Dashboard Monitoring" di header
2. Lihat item per lokasi
3. Klik "Lihat Semua" untuk detail lengkap

##  Fitur UI/UX

- **Toast Notifications**: Notifikasi real-time untuk setiap aksi
- **Modal Confirmations**: Konfirmasi untuk aksi penting (hapus, bulk save)
- **Autocomplete Search**: Pencarian item dengan dropdown suggestions
- **Stock Badges**: Visual indicator untuk level stok (Habis, Rendah, Sedang, Tinggi)
- **Responsive Design**: Optimal di desktop, tablet, dan mobile

## 🔧 Konfigurasi

### Port
Default port: `5000`

**Production (Linux):**
Edit `start_production.sh`:
```bash
gunicorn -w 4 -b 0.0.0.0:8080 app:app  # Ubah 5000 ke 8080
```

**Production (Windows):**
Edit `start_production.bat`:
```batch
python -m gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

**Development:**
Edit `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Workers (Production)
Jumlah worker processes untuk handle concurrent requests.

**Recommended:** 2-4 x CPU cores

**Linux - Edit `start_production.sh`:**
```bash
gunicorn -w 8 -b 0.0.0.0:5000 app:app  # 8 workers
```

**Windows - Edit `start_production.bat`:**
```batch
python -m gunicorn -w 8 -b 0.0.0.0:5000 app:app
```

### Database Location
Default: `atk.db` di root folder

Ubah di `app.py`:
```python
conn = sqlite3.connect('atk.db')
```

##  Troubleshooting

### Error: Port Already in Use

**Linux/Mac:**
```bash
# Cek yang menggunakan port
lsof -i :5000

# Stop production server
./stop_production.sh

# Atau kill manual
pkill -f "gunicorn.*app:app"
```

**Windows:**
```cmd
# Cek yang menggunakan port
netstat -ano | findstr :5000

# Stop production server
stop_production.bat

# Atau kill manual
taskkill /F /PID [PID_NUMBER]
```

### Database Locked Error

**Linux/Mac:**
```bash
./stop_production.sh
./start_production.sh
```

**Windows:**
```cmd
stop_production.bat
start_production.bat
```

### Import Error / Module Not Found
```bash
pip install -r requirements.txt
```

### Production Server Tidak Jalan

**1. Cek log error:**

Linux:
```bash
cat error.log
cat gunicorn.log
```

Windows:
```cmd
type error.log
type gunicorn.log
```

**2. Test Gunicorn manual:**

Linux:
```bash
gunicorn -w 1 -b 127.0.0.1:5000 app:app
```

Windows:
```cmd
python -m gunicorn -w 1 -b 127.0.0.1:5000 app:app
```

**3. Pastikan Gunicorn terinstall:**
```bash
pip show gunicorn
```

Jika belum:
```bash
pip install gunicorn==21.2.0
```

### Performance Lambat

**Increase worker count:**

Linux - Edit `start_production.sh`:
```bash
gunicorn -w 8 -b 0.0.0.0:5000 app:app
```

Windows - Edit `start_production.bat`:
```batch
python -m gunicorn -w 8 -b 0.0.0.0:5000 app:app
```

**Monitor resource usage:**

Linux:
```bash
./status_production.sh
```

Windows:
```cmd
status_production.bat
```

## 📝 Development

### Menjalankan dalam Mode Debug
Edit `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

⚠️ **WARNING**: JANGAN enable debug di production!

### Struktur Kode

**Backend (`app.py`):**
- Context manager untuk koneksi database aman
- Error handling di setiap endpoint
- Validasi input di server-side

**Frontend:**
- `app.js`: Logika utama (CRUD, bulk operations)
- `dashboard.js`: Logika dashboard
- `toast.js`: Sistem notifikasi
- `style.css`: Styling lengkap

### Testing Production Locally

**Linux/Mac:**
```bash
./start_production.sh
./status_production.sh
tail -f access.log
./stop_production.sh
```

**Windows:**
```cmd
start_production.bat
status_production.bat
powershell Get-Content access.log -Wait
stop_production.bat
```

## 🔒 Security Checklist

✅ **Production Mode:**
- [x] Gunakan Gunicorn (bukan Flask dev server)
- [x] Disable debug mode
- [x] Set proper file permissions
- [x] Regular backup database
- [x] Monitor error logs

❌ **JANGAN Lakukan:**
- [ ] Gunakan `python app.py` untuk production
- [ ] Enable `debug=True` di production
- [ ] Expose database file ke public
- [ ] Ignore error logs

## 📋 Quick Reference

### Linux/Mac Commands

| Action | Command |
|--------|---------|
| Start Production | `./start_production.sh` |
| Stop Production | `./stop_production.sh` |
| Check Status | `./status_production.sh` |
| View Access Log | `tail -f access.log` |
| View Error Log | `tail -f error.log` |

### Windows Commands

| Action | Command |
|--------|---------|
| Start Production | `start_production.bat` |
| Stop Production | `stop_production.bat` |
| Check Status | `status_production.bat` |
| View Access Log | `powershell Get-Content access.log -Wait` |
| View Error Log | `powershell Get-Content error.log -Wait` |

## 📄 License

Project ini dibuat untuk keperluan internal Timbangan.

## 👥 Support

Untuk pertanyaan atau masalah, hubungi Huda Timbangan.

---

**Version:** 1.0.0  
**Last Updated:** Februari 2026  
**Production Ready:** ✅ YES (Linux & Windows)
