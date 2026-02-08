#  ATK Dashboard - Aplikasi Timbangan

Sistem manajemen inventaris internal untuk Alat Tulis Kantor (ATK).

##  Cara Menjalankan (Run)

###  Windows
Cukup double-click file **`start_production.bat`**
- Server berjalan di background (Silent Mode).
- Buka browser: `http://localhost:5000`

###  Linux / Mac
Buka terminal dan jalankan:
```bash
./start_production.sh
```

---

##  Fitur Utama
- **Dashboard**: Monitoring stok per lokasi penyimpanan.
- **Inventori**: Tambah barang, edit, dan hapus.
- **Transaksi**: Catat barang masuk (Reservasi) dan barang keluar (Pemakaian).
- **Laporan**: Export laporan bulanan ke Excel/CSV.

---

##  Backup Database
Agar data aman, jalankan script backup secara berkala:
- **Windows**: Double-click `backup_db.bat`
- **Linux**: Jalankan `./backup_db.sh`

File backup akan muncul di folder `backups/` dengan nama tangga & jam.
*Lihat panduan lengkap di `BACKUP_GUIDE.md`*

---

##  Tech Stack
- Python (Flask)
- SQLite Database
- Waitress Server (Production-ready)
