# 📊 ATK Dashboard - Sistem Manajemen Inventaris

Aplikasi **ATK Dashboard** adalah sistem manajemen inventaris terintegrasi yang dirancang khusus untuk mengelola stok **Alat Tulis Kantor (ATK)** dengan efisien. Aplikasi ini menyediakan dashboard real-time, pencatatan transaksi otomatis, dan laporan komprehensif untuk memudahkan monitoring stok barang di berbagai lokasi penyimpanan.

---

## Daftar Isi

- [Tentang Aplikasi](#tentang-aplikasi)
- [Fitur Utama](#fitur-utama)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Instalasi Windows](#instalasi-windows)
- [Quick Start](#quick-start)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Backup Database](#backup-database)
- [Tech Stack](#tech-stack)
- [Troubleshooting](#troubleshooting)

---

## Tentang Aplikasi

ATK Dashboard adalah solusi manajemen inventaris untuk:
- **Warehouse** - Catat transaksi barang masuk dan keluar

**Keunggulan:**
- ✅ Interface user-friendly dan responsif
- ✅ Pencatatan transaksi real-time
- ✅ Export laporan ke Excel/CSV
- ✅ Backup database otomatis
- ✅ Monitoring stok dari berbagai lokasi
- ✅ Lightweight dan cepat

---

## Fitur Utama

### 1. Dashboard
- Visualisasi stok barang per lokasi penyimpanan
- Monitoring real-time kondisi inventaris
- Grafik dan statistik stok barang
- Alert untuk stok yang menipis

### 2. Manajemen Inventori
- Tambah barang baru dengan detail lengkap
- Edit informasi barang (nama, MID, storage location, dll)
- Hapus barang yang sudah tidak digunakan
- Pencarian dan filter barang yang cepat
- Organisasi berdasarkan kategori dan lokasi penyimpanan

### 3. Transaksi
- **Barang Masuk (Reservasi)**: Catat pengadaan barang baru
- **Barang Keluar (Pemakaian)**: Catat penggunaan atau pengeluaran barang
- Riwayat transaksi lengkap dan terstruktur
- Pencatatan tanggal, waktu, dan pengguna otomatis

### 4. Laporan & Ekspor
- Generate laporan bulanan/periode
- Export ke format Excel (.xlsx)
- Export ke format CSV (.csv)
- Laporan detail dengan analisis stok
- Print-friendly reports

---

## Persyaratan Sistem

### Minimum Requirements
- **OS**: Windows 7 SP1 atau lebih baru / Linux / macOS
- **RAM**: 512MB (recommended 2GB)
- **Disk Space**: 500MB (termasuk backup)
- **Browser**: Chrome, Firefox, Edge, Safari (versi terbaru)
- **Python**: 3.7 atau lebih baru (untuk development)

### Network
- Localhost access (tidak memerlukan internet)
- Port 5000

---

## Instalasi Windows

### Step 1: Download & Ekstrak File
1. Download project dari GitHub atau dari huda timbangan
2. Ekstrak ke folder yang diinginkan, contoh: `C:\Users\YourUsername\ATK-Dashboard`

### Step 2: Instalasi Python
1. Download Python 3.9+ dari [python.org](https://www.python.org/downloads/)
2. **PENTING**: Centang `Add Python to PATH` saat instalasi
3. Klik `Install Now`
4. Tunggu hingga instalasi selesai

### Step 3: Instalasi Dependencies
1. Buka Command Prompt (Win + R, ketik `cmd`, Enter)
2. Navigate ke folder project:
   ```cmd
   cd C:\Users\YourUsername\ATK-Dashboard
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
4. Tunggu hingga semua package terinstall

### Step 4: Jalankan Aplikasi
1. Double-click file `run.bat`
2. Atau dari Command Prompt:
   ```cmd
   python waitress_server.py
   ```
3. Aplikasi akan berjalan di http://localhost:5000
4. Buka browser dan akses aplikasi

### Step 5 (Optional): Backup Database
- Untuk backup manual, double-click `backup_db.bat`
- Untuk backup otomatis, ikuti panduan Backup Otomatis di bawah

---

## Quick Start

### Pertama Kali Menjalankan

**Windows:**
```bash
# Cara 1: Double-click file
run.bat

# Cara 2: Command Prompt
python waitress_server.py
```

Kemudian buka browser dan akses: **http://localhost:5000**

### Stop Aplikasi
- Tekan `Ctrl + C` di Command Prompt/Terminal
- Atau double-click `stop.bat` (Windows)

---

## Panduan Penggunaan

### 1. Dashboard
1. Buka aplikasi di http://localhost:5000
2. klik **Lihat Dashboard Monitoring** Anda akan melihat dashboard utama dengan overview stok
3. Pantau barang-barang dengan stok menipis

### 2. Menambah Barang Baru (Inventori)
1. Klik menu **"Inventori"**
2. Isi form dengan data lengkap:
   - **MID**: Kode unik barang (misal: "900123")
   - **Nama Barang**: Nama item (misal: "Pulpen Biru")
   - **Stok**: Jumlah barang yang tersedia
   - **Satuan**: Satuan barang(misal: pcs, box, dll)
   - **Lokasi**: Tempat penyimpanan (misal: "Rak A-1")
3. Klik **"Tambah item"**

### 3. Edit Barang
1. Cari barang di daftar inventori
2. Klik tombol **"Edit"**
3. Ubah data yang diperlukan
4. Klik **"Simpan"**

### 4. Mencatat Barang Masuk (Reservasi)
1. Klik menu **"Inventori"** → **"Reservasi stock"**
2. Pilih barang dari dropdown
3. Isi jumlah yang masuk
4. Klik **"Simpan Semua Reservasi"**
5. Stok barang akan otomatis bertambah

### 5. Mencatat Barang Keluar (Pemakaian)
1. Klik menu **"Inventori"** → **"Stock"**
2. Pilih barang dari **Daftar ATK**
3. klik **Kurangi Stok**
4. Isi jumlah yang keluar
5. Klik **"Simpan"**
6. Stok barang akan otomatis berkurang

### 6. Melihat Riwayat Transaksi
1. Klik menu **"Laporan Bulanan"**
2. Lihat semua transaksi dengan filter priode

### 7. Export Laporan
1. Klik menu **"Laporan Bulanan"**
2. Pilih periode laporan (bulan/tahun)
4. Klik **"Export CSV"**
5. File akan tersimpan di folder Downloads

### 8. Hapus Barang
1. Cari barang di **inventori** _ **Stock**
2. Klik tombol **"Hapus"** (ikon trash)
3. Konfirmasi penghapusan
4. Barang akan dihapus dari sistem

---

## Backup Database

### Backup Manual

**Windows:**
```bash
Double-click backup_db.bat
```

File backup akan disimpan di folder `backups/` dengan format nama: `YYYY-MM-DD_HH-MM-SS.db`

### Backup Otomatis (Windows)

Untuk membuat backup otomatis setiap hari:

#### Metode 1: Menggunakan Task Scheduler (Recommended)

1. **Buka Task Scheduler**
   - Tekan `Win + R`
   - Ketik `taskschd.msc`
   - Tekan `Enter`

2. **Buat Task Baru**
   - Di panel kanan, klik "Create Basic Task"

3. **Isi Identitas Task**
   - Nama: `ATK Dashboard Backup Harian`
   - Deskripsi: `Backup database ATK Dashboard setiap hari pukul 09:00`

4. **Atur Trigger (Jadwal)**
   - Pilih: **Daily**
   - Mulai: [tanggal hari ini]
   - Berulang setiap: 1 hari
   - Jam: 09:00 (sesuaikan jam yang diinginkan)

5. **Atur Action (Aksi)**
   - Action: **Start a program**
   - Program/script: `C:\Windows\System32\cmd.exe`
   - Add arguments (optional): `/c "C:\Users\YourUsername\ATK-Dashboard\backup_db.bat"`
   - Ganti path dengan lokasi project Anda

6. **Selesai**
   - Review summary dan klik **Finish**

#### Metode 2: Menggunakan Windows Event Scheduler (Advanced)

Jika Task Scheduler tidak berfungsi, gunakan event log trigger.

### Restore Backup

Jika perlu mengembalikan database dari backup:

1. Buka folder `backups/`
2. Pilih file backup yang diinginkan
3. Copy file tersebut
4. Paste ke folder root project, rename menjadi `atk.db`
5. Restart aplikasi

---

## Tech Stack

### Backend
- **Framework**: Flask 2.x (Python Web Framework)
- **Language**: Python 3.7+
- **Server**: Waitress (Production-ready WSGI server)
- **Database**: SQLite 3

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design, modern styling
- **JavaScript**: Interactive UI dan form validation

### Database Schema
- **Items**: Data barang/inventori
- **Locations**: Lokasi penyimpanan
- **Transactions**: Riwayat transaksi masuk/keluar
- **Backups**: Log backup database

### Dependencies Utama
```
Flask==2.x.x
Flask-SQLAlchemy==3.x.x
Waitress==2.x.x
openpyxl (untuk export Excel)
```

Lihat `requirements.txt` untuk daftar lengkap.

---

## Troubleshooting

### Masalah: "Port 5000 sudah digunakan"
**Solusi:**
```cmd
# Cari proses yang menggunakan port 5000
netstat -ano | findstr :5000

# Stop proses (ganti PID dengan nomor dari hasil di atas)
taskkill /PID <PID> /F
```

### Masalah: "Python tidak ditemukan"
**Solusi:**
- Pastikan Python sudah terinstall dan ditambahkan ke PATH
- Restart Command Prompt setelah instalasi Python
- Coba dengan command: `python --version`

### Masalah: "Module tidak ditemukan"
**Solusi:**
```cmd
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Masalah: Database error atau corrupt
**Solusi:**
- Gunakan file backup (lihat bagian Restore Backup)
- Atau delete file `atk.db` (akan dibuat ulang otomatis)

### Masalah: Aplikasi loading lambat
**Solusi:**
- Tutup browser tabs lain yang tidak perlu
- Clear browser cache (Ctrl + Shift + Delete)
- Restart aplikasi
- Cek resource monitor untuk proses yang menggunakan CPU tinggi

---

## 📞 Support & Maintenance

Untuk pertanyaan atau laporan bug:
- Hubungi Huda timbangan

---

## Changelog

### Version 1.0
- ✅ Dashboard dengan visualisasi stok
- ✅ Manajemen inventori lengkap
- ✅ Sistem transaksi barang masuk/keluar
- ✅ Export laporan Excel/CSV
- ✅ Backup database otomatis

---

## 📄 Lisensi

Aplikasi ini adalah properti internal perusahaan dan tidak boleh didistribusikan tanpa izin.

---

*Last Updated: February 2026*
*Version: 1.0*
