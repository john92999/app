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
