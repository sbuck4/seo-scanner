#!/bin/bash

# SEO Scanner Startup Script
set -e

echo "🔍 Starting SEO Scanner Pro..."

# Create necessary directories
mkdir -p logs reports

# Load environment variables if .env exists
if [ -f .env ]; then
    echo "📋 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default values
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8501}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

echo "🌐 Server will run on ${HOST}:${PORT}"
echo "📊 Log level: ${LOG_LEVEL}"

# Check if this is a development or production environment
if [ "$DEBUG" = "true" ]; then
    echo "🔧 Running in DEBUG mode"
    # Development mode with auto-reload
    streamlit run app.py \
        --server.address ${HOST} \
        --server.port ${PORT} \
        --server.headless true \
        --browser.gatherUsageStats false \
        --logger.level ${LOG_LEVEL}
else
    echo "🚀 Running in PRODUCTION mode"
    # Production mode
    streamlit run app.py \
        --server.address ${HOST} \
        --server.port ${PORT} \
        --server.headless true \
        --browser.gatherUsageStats false \
        --server.maxUploadSize 200 \
        --logger.level ${LOG_LEVEL}
fi