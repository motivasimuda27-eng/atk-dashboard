@echo off
REM ATK Dashboard - Production Stop Script for Windows

echo ========================================
echo   Stopping ATK Dashboard Server
echo ========================================
echo.

REM Kill all Python processes running gunicorn
echo [INFO] Stopping production server...

REM Method 1: Kill by window title (if available)
taskkill /F /FI "WINDOWTITLE eq gunicorn*" >nul 2>&1

REM Method 2: Kill by command line containing gunicorn
for /f "tokens=2" %%a in ('tasklist /v /fo list ^| findstr /i "gunicorn"') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Method 3: Kill Python processes on port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 1 >nul

echo [SUCCESS] Server berhasil dihentikan.
echo.
pause
