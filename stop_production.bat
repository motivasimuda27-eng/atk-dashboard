@echo off
REM ATK Dashboard - Production Stop Script for Windows
REM Stops background server (pythonw.exe processes)

echo ========================================
echo   Stopping ATK Dashboard Server
echo ========================================
echo.

REM Kill Python processes on port 5000
echo [INFO] Stopping production server...

REM Method 1: Kill by port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo [INFO] Killing process on port 5000, PID: %%a
    taskkill /F /PID %%a >nul 2>&1
)

REM Method 2: Kill pythonw.exe running waitress_server.py
echo [INFO] Stopping pythonw processes running waitress_server...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%waitress_server%%'" delete >nul 2>&1
)

REM Method 3: Kill any python.exe running waitress_server
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a and CommandLine like '%%waitress_server%%'" delete >nul 2>&1
)

timeout /t 1 >nul

REM Check if still running
netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo [SUCCESS] Server berhasil dihentikan.
) else (
    echo [WARNING] Masih ada process yang berjalan pada port 5000.
    echo [INFO] Mencoba force kill...
    
    REM Force kill any remaining processes on port 5000
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    
    timeout /t 1 >nul
    
    netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1
    if errorlevel 1 (
        echo [SUCCESS] Server berhasil dihentikan (force kill).
    ) else
        echo [ERROR] Gagal menghentikan server. Silakan cek Task Manager.
    )
)

echo.
pause
