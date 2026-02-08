@echo off
REM ATK Dashboard - View Production Logs

echo ========================================
echo   ATK Dashboard - Production Logs
echo ========================================
echo.
echo Pilih log yang ingin dilihat:
echo.
echo [1] Production Log (Semua aktivitas)
echo [2] Error Log (Hanya errors)
echo [3] Tail - Monitor Real-time (Production Log)
echo [4] Tail - Monitor Real-time (Error Log)
echo [5] Keluar
echo.

choice /C 12345 /N /M "Pilihan [1-5]: "

if errorlevel 5 goto :end
if errorlevel 4 goto :tail_error
if errorlevel 3 goto :tail_production
if errorlevel 2 goto :view_error
if errorlevel 1 goto :view_production

:view_production
cls
echo ========================================
echo   Production Log
echo ========================================
echo.
if exist production.log (
    type production.log
) else (
    echo [INFO] File production.log tidak ditemukan.
    echo        Jalankan server terlebih dahulu.
)
echo.
pause
goto :end

:view_error
cls
echo ========================================
echo   Error Log
echo ========================================
echo.
if exist production_error.log (
    for %%F in (production_error.log) do set size=%%~zF
    if %size% GTR 0 (
        type production_error.log
    ) else (
        echo [INFO] Tidak ada error. Server berjalan normal!
    )
) else (
    echo [INFO] File production_error.log tidak ditemukan.
    echo        Jalankan server terlebih dahulu.
)
echo.
pause
goto :end

:tail_production
cls
echo ========================================
echo   Monitor Real-time - Production Log
echo   Press Ctrl+C to stop
echo ========================================
echo.
if exist production.log (
    powershell -Command "Get-Content production.log -Wait -Tail 20"
) else (
    echo [INFO] File production.log tidak ditemukan.
    pause
)
goto :end

:tail_error
cls
echo ========================================
echo   Monitor Real-time - Error Log
echo   Press Ctrl+C to stop
echo ========================================
echo.
if exist production_error.log (
    powershell -Command "Get-Content production_error.log -Wait -Tail 20"
) else (
    echo [INFO] File production_error.log tidak ditemukan.
    pause
)
goto :end

:end
