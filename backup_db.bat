@echo off
setlocal EnableDelayedExpansion

REM ATK Dashboard - Database Backup Script
REM Backs up atk.db to 'backups' folder with timestamp

REM Set current directory to script location
cd /d "%~dp0"

REM Create backup directory if not exists
if not exist "backups" mkdir "backups"

REM Get current date and time for filename
REM Format: YYYY-MM-DD_HH-MM-SS
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "timestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%"

set "backup_file=backups\atk_%timestamp%.db"

echo [INFO] Backing up database...
copy "atk.db" "%backup_file%" >nul

if %errorlevel% equ 0 (
    echo [SUCCESS] Backup created at: %backup_file%
) else (
    echo [ERROR] Failed to backup database!
    exit /b 1
)

REM Cleanup old backups (older than 30 days)
echo [INFO] Cleaning up old backups...
forfiles /p "backups" /s /m atk_*.db /d -30 /c "cmd /c del @path" 2>nul

echo [DONE] Backup process completed.
timeout /t 5 >nul
