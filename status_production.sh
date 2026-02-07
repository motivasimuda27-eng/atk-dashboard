#!/bin/bash

# ATK Dashboard - Production Status Script

echo "📊 ATK Dashboard Production Status"
echo "=================================="
echo ""

# Check if gunicorn is running
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo "✅ Status: RUNNING"
    echo ""
    
    # Show process info
    echo "🔍 Process Information:"
    ps aux | grep "gunicorn.*app:app" | grep -v grep | awk '{printf "   PID: %s | CPU: %s%% | MEM: %s%% | CMD: %s\n", $2, $3, $4, $11}'
    echo ""
    
    # Show listening port
    echo "🌐 Network:"
    echo "   Listening on: http://0.0.0.0:5000"
    echo "   Local URL:    http://127.0.0.1:5000"
    echo "   Network URL:  http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    
    # Show log files
    echo "📝 Log Files:"
    if [ -f access.log ]; then
        LINES=$(wc -l < access.log)
        echo "   - access.log: $LINES lines"
    fi
    if [ -f error.log ]; then
        SIZE=$(du -h error.log | cut -f1)
        echo "   - error.log: $SIZE"
    fi
    if [ -f gunicorn.log ]; then
        SIZE=$(du -h gunicorn.log | cut -f1)
        echo "   - gunicorn.log: $SIZE"
    fi
    echo ""
    
    # Show recent errors
    if [ -f error.log ] && [ -s error.log ]; then
        echo "⚠️  Recent Errors (last 5 lines):"
        tail -5 error.log | sed 's/^/   /'
    fi
    
else
    echo "❌ Status: NOT RUNNING"
    echo ""
    echo "💡 Untuk menjalankan server, gunakan: ./start_production.sh"
fi
