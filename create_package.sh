#!/bin/bash

# OCR App - Package Creator
# This script creates a downloadable package of your OCR app

echo "📦 Creating OCR App Package..."

# Create temporary directory
PACKAGE_DIR="ocr-text-extractor-$(date +%Y%m%d)"
mkdir -p "$PACKAGE_DIR"

echo "📁 Copying files..."

# Copy backend
cp -r backend "$PACKAGE_DIR/"
rm -rf "$PACKAGE_DIR/backend/__pycache__"
rm -rf "$PACKAGE_DIR/backend/.env"  # Don't include .env

# Copy frontend (excluding node_modules and build artifacts)
mkdir -p "$PACKAGE_DIR/frontend"
cp -r frontend/app "$PACKAGE_DIR/frontend/"
cp -r frontend/assets "$PACKAGE_DIR/frontend/"
cp -r frontend/scripts "$PACKAGE_DIR/frontend/"
cp frontend/package.json "$PACKAGE_DIR/frontend/"
cp frontend/app.json "$PACKAGE_DIR/frontend/"
cp frontend/eas.json "$PACKAGE_DIR/frontend/"
cp frontend/tsconfig.json "$PACKAGE_DIR/frontend/"
cp frontend/eslint.config.js "$PACKAGE_DIR/frontend/"
cp frontend/metro.config.js "$PACKAGE_DIR/frontend/"
cp frontend/.gitignore "$PACKAGE_DIR/frontend/"

# Copy documentation
cp BUILD_INSTRUCTIONS.md "$PACKAGE_DIR/"
cp README_APP.md "$PACKAGE_DIR/README.md"

# Create .env template
cat > "$PACKAGE_DIR/frontend/.env.example" << 'EOF'
# Update this with your local backend URL when running
# Find your local IP: ifconfig (Mac/Linux) or ipconfig (Windows)
EXPO_PUBLIC_BACKEND_URL=http://YOUR_LOCAL_IP:8001
EOF

# Create backend .env template
cat > "$PACKAGE_DIR/backend/.env.example" << 'EOF'
# MongoDB URL (optional - only if you want to use MongoDB)
MONGO_URL=mongodb://localhost:27017
DB_NAME=ocr_app
EOF

# Create quick start script for Mac/Linux
cat > "$PACKAGE_DIR/quickstart.sh" << 'EOF'
#!/bin/bash

echo "🚀 OCR Text Extractor - Quick Start"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    echo "   Download from: https://nodejs.org"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

echo "✅ Node.js and Python found"
echo ""

# Setup frontend
echo "📱 Setting up Frontend..."
cd frontend
yarn install || npm install
cd ..

# Setup backend
echo "🖥️  Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Read BUILD_INSTRUCTIONS.md for building the app"
echo "   2. To build for Android: cd frontend && eas build --platform android --profile preview"
echo "   3. To run backend: cd backend && source venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8001"
echo ""
EOF

chmod +x "$PACKAGE_DIR/quickstart.sh"

# Create quick start script for Windows
cat > "$PACKAGE_DIR/quickstart.bat" << 'EOF'
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
EOF

# Create archive
echo "🗜️  Creating archive..."
tar -czf "${PACKAGE_DIR}.tar.gz" "$PACKAGE_DIR"
zip -r "${PACKAGE_DIR}.zip" "$PACKAGE_DIR" > /dev/null 2>&1

echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Download one of these files:"
echo "   • ${PACKAGE_DIR}.tar.gz  (Linux/Mac)"
echo "   • ${PACKAGE_DIR}.zip     (Windows/All)"
echo ""
echo "📍 Location: $(pwd)"
echo ""
echo "🚀 On your laptop:"
echo "   1. Extract the archive"
echo "   2. Run quickstart.sh (Mac/Linux) or quickstart.bat (Windows)"
echo "   3. Follow BUILD_INSTRUCTIONS.md to build the app"
echo ""
