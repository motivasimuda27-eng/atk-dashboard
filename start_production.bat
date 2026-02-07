@echo off
REM ATK Dashboard - Production Startup Script for Windows

echo ========================================
echo   ATK Dashboard - Production Mode
echo ========================================
echo.

REM Check if gunicorn is installed
pip show gunicorn >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Gunicorn tidak ditemukan. Installing...
    pip install gunicorn==21.2.0
    echo.
)

REM Kill existing gunicorn process if any
echo [INFO] Checking for existing processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq gunicorn*" >nul 2>&1
timeout /t 1 >nul

REM Start gunicorn in background
echo [SUCCESS] Starting Gunicorn server...
start /B python -m gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile access.log --error-logfile error.log app:app

REM Wait for server to start
timeout /t 3 >nul

echo.
echo ========================================
echo   Server berhasil dijalankan!
echo ========================================
echo.
echo [INFO] Informasi Server:
echo   - URL Lokal:    http://127.0.0.1:5000
echo   - URL Network:  http://localhost:5000
echo   - Workers:      4 processes
echo.
echo [INFO] Log Files:
echo   - Access Log:   access.log
echo   - Error Log:    error.log
echo.
echo [TIPS] Buka browser dan akses http://127.0.0.1:5000
echo.
echo [STOP] Untuk menghentikan server: stop_production.bat
echo [STATUS] Untuk cek status: status_production.bat
echo.
pause
