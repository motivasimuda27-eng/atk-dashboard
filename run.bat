@echo off
REM ========================================
REM Jalankan Aplikasi ATK Tanpa CMD Window
REM ========================================

cd /d "%~dp0"

REM Jalankan dengan pythonw.exe (tidak menampilkan console)
start /B pythonw.exe waitress_server.py

REM Beri notifikasi
echo Aplikasi ATK sudah berjalan di background!
echo.
echo Akses di: http://localhost:5000
echo.
echo Untuk menghentikan aplikasi:
echo 1. Buka Task Manager (Ctrl+Shift+Esc)
echo 2. Tab "Details"
echo 3. Cari "pythonw.exe"
echo 4. Klik kanan, pilih "End task"
echo.
timeout /t 5

REM Tutup window ini
exit
