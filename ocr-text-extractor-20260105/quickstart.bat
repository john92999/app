@echo off
echo OCR Text Extractor - Quick Start
echo.

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. Please install Node.js first.
    echo Download from: https://nodejs.org
    exit /b 1
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Please install Python 3 first.
    exit /b 1
)

echo Node.js and Python found
echo.

REM Setup frontend
echo Setting up Frontend...
cd frontend
call yarn install || call npm install
cd ..

REM Setup backend
echo Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo.
echo Setup complete!
echo.
echo Next steps:
echo   1. Read BUILD_INSTRUCTIONS.md for building the app
echo   2. To build for Android: cd frontend ^&^& eas build --platform android --profile preview
echo   3. To run backend: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn server:app --host 0.0.0.0 --port 8001
echo.
pause
