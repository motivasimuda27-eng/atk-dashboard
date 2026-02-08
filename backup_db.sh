#!/bin/bash

# ATK Dashboard - Database Backup Script
# Backs up atk.db to 'backups' folder with timestamp

# Set current directory to script location
cd "$(dirname "$0")"

# Create backup directory if not exists
if [ ! -d "backups" ]; then
    mkdir "backups"
fi

# Get current date and time for filename
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="backups/atk_$TIMESTAMP.db"

echo "[INFO] Backing up database..."

if cp "atk.db" "$BACKUP_FILE"; then
    echo "[SUCCESS] Backup created at: $BACKUP_FILE"
else
    echo "[ERROR] Failed to backup database!"
    exit 1
fi

# Cleanup old backups (older than 30 days)
echo "[INFO] Cleaning up old backups..."
find backups -name "atk_*.db" -mtime +30 -delete 2>/dev/null

echo "[DONE] Backup process completed."
