#!/bin/bash

# ATK Dashboard - Production Startup Script

echo "🚀 Starting ATK Dashboard in Production Mode..."
echo ""

# Warna untuk output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo -e "${YELLOW}⚠️  Gunicorn tidak ditemukan. Installing...${NC}"
    pip install gunicorn==21.2.0
fi

# Kill existing gunicorn process if any
echo "🔍 Checking for existing processes..."
pkill -f "gunicorn.*app:app" 2>/dev/null
sleep 1

# Start gunicorn in background
echo -e "${GREEN}✅ Starting Gunicorn server...${NC}"
nohup gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile access.log --error-logfile error.log app:app > gunicorn.log 2>&1 &

# Get PID
GUNICORN_PID=$!
sleep 2

# Check if process is running
if ps -p $GUNICORN_PID > /dev/null; then
    echo -e "${GREEN}✅ Server berhasil dijalankan!${NC}"
    echo ""
    echo "📋 Informasi Server:"
    echo "   - URL Lokal:    http://127.0.0.1:5000"
    echo "   - URL Network:  http://$(hostname -I | awk '{print $1}'):5000"
    echo "   - Workers:      4 processes"
    echo "   - PID:          $GUNICORN_PID"
    echo ""
    echo "📝 Log Files:"
    echo "   - Access Log:   access.log"
    echo "   - Error Log:    error.log"
    echo "   - Gunicorn Log: gunicorn.log"
    echo ""
    echo "🛑 Untuk menghentikan server, jalankan: ./stop_production.sh"
    echo "📊 Untuk melihat status, jalankan: ./status_production.sh"
    
    # Save PID to file
    echo $GUNICORN_PID > gunicorn.pid
else
    echo -e "${YELLOW}⚠️  Gagal menjalankan server. Cek error.log untuk details.${NC}"
    exit 1
fi
