# OCR Text Extractor Mobile App

## 🎯 What This App Does

Extract text from images, handwritten notes, and documents using your phone's camera - **100% offline!**

### Features:
- 📸 **Camera Capture** - Take photos and extract text instantly
- 🖼️ **Gallery Upload** - Select existing images
- 📄 **PDF Support** - Extract text from PDF pages
- 📋 **Copy to Clipboard** - Quick text copying
- 💾 **Export Options** - Save as TXT or DOCX files
- 🔒 **Privacy First** - No history saved, works offline

---

## ⚠️ Important: This Needs to be Built

This app uses **native OCR engines** (Google ML Kit on Android, Apple Vision on iOS) and **cannot** run in Expo Go preview.

**You must build it as a native app first.**

---

## 🚀 Quick Start - Build Your App

### Step 1: Download the Project Files

You can download all files to your laptop:

**Using Git** (if you have Git installed):
```bash
# Clone or download this repository
git clone <your-repo>
cd <project-folder>
```

**Or** use the download script below to get files via SSH/FTP.

### Step 2: Install Dependencies

```bash
# Navigate to frontend folder
cd frontend

# Install packages
yarn install
# or
npm install
```

### Step 3: Build the App

#### For Android (Easiest):

```bash
# Install EAS CLI
npm install -g eas-cli

# Login (free account)
eas login

# Build APK
eas build --platform android --profile preview
```

This will build your app on Expo's servers. Download the APK when done and install it on your Android phone.

#### For iOS (Mac only):

```bash
# Generate native project
npx expo prebuild --platform ios

# Install dependencies
cd ios && pod install && cd ..

# Open in Xcode
open ios/*.xcworkspace

# Build and run on your iPhone
```

---

## 📱 How to Use the App

1. **Open the app** on your phone
2. **Choose an option**:
   - Take Photo
   - Upload Image  
   - Upload PDF (screenshot pages)
3. **View extracted text** automatically
4. **Export**:
   - Copy to clipboard
   - Save as TXT
   - Save as DOCX (needs backend)

---

## 💻 Backend Setup (Optional - for DOCX export)

The app works fully offline for OCR, but needs a backend for DOCX generation.

### On Your Laptop:

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Connect App to Backend:

1. Find your laptop's local IP:
   - Mac/Linux: `ifconfig | grep inet`
   - Windows: `ipconfig`

2. Update `frontend/.env`:
   ```
   EXPO_PUBLIC_BACKEND_URL=http://YOUR_IP:8001
   ```

---

## 📂 Download Project to Your Laptop

### Method 1: Manual Download

1. Download all files from the `/app` directory
2. Extract to your laptop
3. Follow build instructions above

### Method 2: Using SCP (if SSH access available)

```bash
# From your laptop
scp -r user@host:/app ./ocr-app
cd ocr-app/frontend
yarn install
```

### Method 3: Create Archive

```bash
# On the server
cd /app
tar -czf ocr-app.tar.gz backend frontend BUILD_INSTRUCTIONS.md README_APP.md

# Download ocr-app.tar.gz to your laptop
# Extract and build
```

---

## 🔧 Technologies Used

- **Frontend**: Expo, React Native, TypeScript
- **OCR**: Google ML Kit (Android), Apple Vision (iOS)  
- **Backend**: Python FastAPI, python-docx
- **100% Offline** OCR processing

---

## 📊 App Details

- **Size**: ~40-50 MB (includes ML models)
- **Platforms**: Android & iOS
- **Permissions Needed**: Camera, Photo Library
- **Internet Required**: Only for initial build, not for app usage
- **Handwriting Support**: Limited (better with printed text)

---

## 🆘 Troubleshooting

**"This app only works in development builds"**
→ You're using Expo Go. Build the app using EAS or expo prebuild.

**"Camera permission denied"**
→ Go to Settings > Apps > OCR Text Extractor > Permissions

**"DOCX export failed"**
→ Backend isn't running. TXT export works without backend.

**Build errors**
→ See full BUILD_INSTRUCTIONS.md for detailed troubleshooting

---

## 📖 Full Documentation

See `BUILD_INSTRUCTIONS.md` for:
- Detailed build instructions
- Platform-specific setup
- Advanced configuration
- Complete troubleshooting guide

---

## ✨ Free & Open

This app is free to use for personal and commercial projects.

**No data collection • No history • No cloud • No tracking**
