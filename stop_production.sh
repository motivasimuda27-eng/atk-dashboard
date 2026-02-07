#!/bin/bash

# ATK Dashboard - Production Stop Script

echo "🛑 Stopping ATK Dashboard Production Server..."

# Kill all gunicorn processes related to this app
pkill -f "gunicorn.*app:app"

# Wait a moment
sleep 1

# Check if still running
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo "⚠️  Force killing remaining processes..."
    pkill -9 -f "gunicorn.*app:app"
fi

# Remove PID file if exists
rm -f gunicorn.pid

echo "✅ Server berhasil dihentikan."
