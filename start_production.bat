@echo off
REM ATK Dashboard - Production Startup Script for Windows (Silent Mode)
REM Runs server in background without console window

echo ========================================
echo   ATK Dashboard - Production Mode
echo   Silent Background Server
echo ========================================
echo.

REM Check if waitress is installed
pip show waitress >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Waitress tidak ditemukan. Installing...
    pip install waitress==3.0.0
    echo.
)

REM Kill existing Python processes on port 5000
echo [INFO] Checking for existing processes on port 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo [INFO] Stopping process PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 1 >nul

REM Check if VBScript exists, if not create it
if not exist "start_production_silent.vbs" (
    echo [INFO] Creating silent starter script...
    (
        echo Set WshShell = CreateObject("WScript.Shell"^)
        echo Set fso = CreateObject("Scripting.FileSystemObject"^)
        echo scriptDir = fso.GetParentFolderName(WScript.ScriptFullName^)
        echo pythonwCmd = "pythonw.exe"
        echo WshShell.Run """" ^& pythonwCmd ^& """ """ ^& scriptDir ^& "\waitress_server.py""", 0, False
        echo WshShell.Popup "ATK Dashboard Production Server started ^& vbCrLf ^& vbCrLf ^& "URL: http://127.0.0.1:5000" ^& vbCrLf ^& vbCrLf ^& "Use stop_production.bat to stop", 5, "ATK Dashboard", 64
    ) > start_production_silent.vbs
)

echo [SUCCESS] Starting server in background (no window)...
echo.

REM Run VBScript to start server silently
cscript //nologo start_production_silent.vbs

REM Wait a bit for server to start
timeout /t 3 >nul

echo ========================================
echo   Server berhasil dijalankan!
echo   (Running in background, no window)
echo ========================================
echo.
echo [INFO] Informasi Server:
echo   - URL Lokal:    http://127.0.0.1:5000
echo   - URL Network:  http://localhost:5000
echo   - Threads:      4 threads
echo   - Mode:         Background (No Console Window)
echo.
echo [INFO] Log Files:
echo   - Server Log:   production.log
echo   - Error Log:    production_error.log
echo.
echo [TIPS] Server berjalan di background tanpa window
echo        Buka browser: http://127.0.0.1:5000
echo.
echo [STOP] Untuk menghentikan: stop_production.bat
echo [STATUS] Untuk cek status: status_production.bat
echo.
echo Popup notification akan muncul sebentar...
echo.
pause
