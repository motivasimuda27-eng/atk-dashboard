@echo off
REM ========================================
REM Hentikan Aplikasi ATK yang berjalan
REM ========================================

echo ========================================
echo   MENGHENTIKAN APLIKASI ATK
echo ========================================
echo.

REM Cari dan hentikan process pythonw.exe yang menjalankan app.py
echo [INFO] Mencari aplikasi yang berjalan...

tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Aplikasi ditemukan, menghentikan...
    taskkill /F /IM pythonw.exe /T >NUL 2>&1
    echo [OK] Aplikasi berhasil dihentikan!
) else (
    echo [INFO] Tidak ada aplikasi yang sedang berjalan
)

echo.
echo ========================================
timeout /t 3
