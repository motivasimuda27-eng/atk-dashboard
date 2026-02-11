"""
ATK Dashboard - Production WSGI Server (Windows)
Uses Waitress - A production-quality pure-Python WSGI server.
Runs silently in background with file logging.
"""

import sys
import os
import logging
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
from app import app

# Setup logging to file
ERROR_LOG_FILE = 'error.log'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Also print to console if visible
    ]
)

# Error logging
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(error_handler)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('=' * 50)
    logger.info('  ATK Dashboard Production Server')
    logger.info('  Using Waitress WSGI Server')
    logger.info('  Mode: Background (Silent)')
    logger.info('=' * 50)
    logger.info('')
    logger.info('[SUCCESS] Server is starting...')
    logger.info('[INFO] URL Lokal:    http://127.0.0.1:5000')
    logger.info('[INFO] URL Network:  http://0.0.0.0:5000')
    logger.info('[INFO] Threads:      4 threads')
    logger.info('[INFO] Error Log:    %s', ERROR_LOG_FILE)
    logger.info('')
    logger.info('[INFO] Server started at: %s', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info('=' * 50)
    logger.info('')
    
    try:
        # Start Waitress server
        # threads: Number of threads used to process application logic
        # channel_timeout: Maximum time to wait for a new request on an open connection
        serve(
            app, 
            host='0.0.0.0', 
            port=5000, 
            threads=4,
            channel_timeout=120,
            cleanup_interval=30,
            url_scheme='http'
        )
    except Exception as e:
        logger.error('[ERROR] Server crashed: %s', str(e))
        logger.error('[ERROR] Stopping server...')
        raise
