@echo off
REM SEO Scanner Startup Script for Windows
echo 🔍 Starting SEO Scanner Pro...

REM Create necessary directories
if not exist logs mkdir logs
if not exist reports mkdir reports

REM Set default values
if "%HOST%"=="" set HOST=0.0.0.0
if "%PORT%"=="" set PORT=8501
if "%LOG_LEVEL%"=="" set LOG_LEVEL=INFO

echo 🌐 Server will run on %HOST%:%PORT%
echo 📊 Log level: %LOG_LEVEL%

REM Check if this is development or production
if "%DEBUG%"=="true" (
    echo 🔧 Running in DEBUG mode
    streamlit run app.py --server.address %HOST% --server.port %PORT% --server.headless true --browser.gatherUsageStats false --logger.level %LOG_LEVEL%
) else (
    echo 🚀 Running in PRODUCTION mode
    streamlit run app.py --server.address %HOST% --server.port %PORT% --server.headless true --browser.gatherUsageStats false --server.maxUploadSize 200 --logger.level %LOG_LEVEL%
)