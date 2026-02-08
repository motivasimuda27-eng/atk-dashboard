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
    echo [STATUS] Server: RUNNING (Background Mode)
    echo.
    
    REM Show process info
    echo [INFO] Process Information:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
        echo   PID: %%a
        
        REM Check if it's pythonw (background) or python (console)
        tasklist /FI "PID eq %%a" | findstr "pythonw.exe" >nul
        if not errorlevel 1 (
            echo   Type: pythonw.exe (Background - No Window)
        ) else (
            tasklist /FI "PID eq %%a" | findstr "python.exe" >nul
            if not errorlevel 1 (
                echo   Type: python.exe (Console Window)
            )
        )
        
        tasklist /FI "PID eq %%a" /FO TABLE /NH
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
    if exist production.log (
        for %%F in (production.log) do echo   - production.log: %%~zF bytes
    )
    if exist production_error.log (
        for %%F in (production_error.log) do (
            set /a size=%%~zF
            if %%~zF gtr 0 (
                echo   - production_error.log: %%~zF bytes [HAS ERRORS!]
            ) else (
                echo   - production_error.log: %%~zF bytes [No errors]
            )
        )
    )
    echo.
    
    REM Show last few lines of log
    if exist production.log (
        echo [INFO] Last 5 log entries:
        powershell -Command "Get-Content production.log -Tail 5"
        echo.
    )
    
    REM Check for recent errors
    if exist production_error.log (
        for %%F in (production_error.log) do set size=%%~zF
        if !size! gtr 0 (
            echo [WARNING] Recent Errors detected!
            echo [INFO] Last 3 error entries:
            powershell -Command "Get-Content production_error.log -Tail 3"
            echo.
        )
    )
)

echo.
pause
