@echo off
REM ATK Dashboard - Production Status Script for Windows

echo ========================================
echo   ATK Dashboard Production Status
echo ========================================
echo.

REM Check if server is running on port 5000
netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1

if errorlevel 1 (
    echo [STATUS] Server: NOT RUNNING
    echo.
    echo [INFO] Untuk menjalankan server, gunakan: start_production.bat
) else (
    echo [STATUS] Server: RUNNING
    echo.
    
    REM Show process info
    echo [INFO] Process Information:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
        echo   PID: %%a
        tasklist /FI "PID eq %%a" /FO TABLE
    )
    echo.
    
    REM Show network info
    echo [INFO] Network:
    echo   Listening on: http://0.0.0.0:5000
    echo   Local URL:    http://127.0.0.1:5000
    echo   Network URL:  http://localhost:5000
    echo.
    
    REM Show log files
    echo [INFO] Log Files:
    if exist access.log (
        for %%F in (access.log) do echo   - access.log: %%~zF bytes
    )
    if exist error.log (
        for %%F in (error.log) do echo   - error.log: %%~zF bytes
    )
    if exist gunicorn.log (
        for %%F in (gunicorn.log) do echo   - gunicorn.log: %%~zF bytes
    )
    echo.
    
    REM Show recent errors
    if exist error.log (
        for %%F in (error.log) do set size=%%~zF
        if !size! gtr 0 (
            echo [WARNING] Recent Errors detected in error.log
            echo Check error.log for details.
        )
    )
)

echo.
pause
