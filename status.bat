@echo off
REM ========================================
REM Cek Status Aplikasi ATK
REM ========================================

echo ========================================
echo   STATUS APLIKASI ATK
echo ========================================
echo.

REM Cek apakah aplikasi sedang berjalan
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [STATUS] Aplikasi SEDANG BERJALAN
    echo.
    echo Process yang berjalan:
    tasklist /FI "IMAGENAME eq pythonw.exe"
    echo.
    echo Akses aplikasi di: http://localhost:5000
) else (
    echo [STATUS] Aplikasi TIDAK BERJALAN
    echo.
    echo Untuk menjalankan aplikasi:
    echo - Double-click "jalankan_tanpa_cmd.bat"
)

echo.
echo ========================================
pause
