# 🎯 COMPLETE SETUP GUIDE - OCR Text Extractor App

## ⚡ TL;DR - Quick Instructions

1. **Download files**: Use `ocr-text-extractor-YYYYMMDD.tar.gz` or `.zip`
2. **Extract and setup**: Run `quickstart.sh` (Mac/Linux) or `quickstart.bat` (Windows)
3. **Build app**: `cd frontend && eas build --platform android --profile preview`
4. **Install APK** on your Android phone
5. **Done!** App works 100% offline for OCR

---

## 📦 Step-by-Step Guide

### 1️⃣ Download the Project

Two package files are available in `/app` directory:
- `ocr-text-extractor-YYYYMMDD.tar.gz` (for Mac/Linux)
- `ocr-text-extractor-YYYYMMDD.zip` (for Windows/All)

Download either file to your laptop.

### 2️⃣ Extract Files

**Mac/Linux:**
```bash
tar -xzf ocr-text-extractor-YYYYMMDD.tar.gz
cd ocr-text-extractor-YYYYMMDD
```

**Windows:**
- Right-click the ZIP file
- Select "Extract All"
- Open the extracted folder

### 3️⃣ Install Dependencies

**Easy Way** - Use the quickstart script:

**Mac/Linux:**
```bash
chmod +x quickstart.sh
./quickstart.sh
```

**Windows:**
- Double-click `quickstart.bat`

**Manual Way:**

```bash
# Frontend
cd frontend
npm install  # or yarn install

# Backend (optional - only for DOCX export)
cd ../backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4️⃣ Build the Mobile App

#### For Android (Recommended - Easiest):

```bash
cd frontend

# Install EAS CLI globally (one time only)
npm install -g eas-cli

# Login to Expo (create free account at expo.dev)
eas login

# Build APK
eas build --platform android --profile preview
```

**Wait 10-20 minutes** for the build to complete on Expo's servers.

When done, you'll get a **download link** for your APK file.

#### For iOS (Mac only):

```bash
cd frontend

# Install CocoaPods (one time only)
sudo gem install cocoapods

# Generate native iOS project
npx expo prebuild --platform ios

# Install iOS dependencies
cd ios
pod install
cd ..

# Open in Xcode
open ios/*.xcworkspace
```

In Xcode:
1. Select your development team
2. Connect your iPhone
3. Click the "Play" button to build and install

### 5️⃣ Install the App

**Android:**
1. Download the APK to your phone
2. Open the APK file
3. Tap "Install"
4. If blocked, go to Settings > Security > Enable "Unknown Sources"

**iOS:**
- App installs directly from Xcode to your connected iPhone

### 6️⃣ Use the App!

**No backend needed for basic OCR!**

1. Open the app
2. Tap "Take Photo" or "Upload Image"
3. Text extracts automatically
4. Copy to clipboard or save as TXT

---

## 🖥️ Backend Setup (Optional)

**Only needed for DOCX export.** TXT export works without backend.

### Start Backend on Your Laptop:

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start server
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Connect Mobile App to Backend:

1. Find your laptop's local IP address:
   - **Mac/Linux**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - Example: `192.168.1.100`

2. Before building the app, update `frontend/.env`:
   ```
   EXPO_PUBLIC_BACKEND_URL=http://192.168.1.100:8001
   ```

3. Rebuild the app with `eas build`

**Note**: Your phone and laptop must be on the **same WiFi network**.

---

## 🎨 What You Get

### App Features:
- ✅ Camera capture
- ✅ Gallery image selection
- ✅ PDF page extraction (screenshot PDF pages)
- ✅ Instant text recognition
- ✅ Copy to clipboard
- ✅ Export as TXT (offline)
- ✅ Export as DOCX (needs backend)

### Technology:
- **OCR Engine**: Google ML Kit (Android), Apple Vision (iOS)
- **Accuracy**: 85-95% for printed text, limited for handwriting
- **Offline**: 100% offline OCR processing
- **Size**: ~40-50 MB app

---

## 🔧 Troubleshooting

### Build Issues

**"eas: command not found"**
```bash
npm install -g eas-cli
```

**"Unauthorized request"**
```bash
eas login
```

**"Build failed - invalid credentials"**
- Make sure you're logged into Expo: `eas whoami`
- Create account at expo.dev if needed

**"Expo CLI version mismatch"**
```bash
npm install -g eas-cli@latest
cd frontend && npx expo install --fix
```

### App Issues

**"Text extraction not supported"**
- You're using Expo Go. Build the app properly with EAS.

**"Camera permission denied"**
- Settings > Apps > OCR Text Extractor > Permissions > Enable Camera

**"DOCX export failed"**
- Backend not running, or wrong IP in .env
- TXT export works without backend

**App won't install on Android**
- Settings > Security > Enable "Install Unknown Apps" for your file manager

### Backend Issues

**"Port 8001 already in use"**
```bash
# Kill the process using port 8001
lsof -ti:8001 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8001   # Windows (note the PID, then: taskkill /PID <PID> /F)
```

**"ModuleNotFoundError: No module named 'docx'"**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📱 Alternative Build Methods

### Method 1: Local Android Build (Advanced)

Requires: Android Studio, JDK 17

```bash
cd frontend
npx expo prebuild --platform android
# Open 'android' folder in Android Studio
# Build > Build Bundle(s) / APK(s) > Build APK(s)
```

### Method 2: Expo Application Services (Easiest)

Already covered above - recommended method!

### Method 3: Manual Gradle Build

```bash
cd frontend
npx expo prebuild --platform android
cd android
./gradlew assembleRelease
# APK in: android/app/build/outputs/apk/release/
```

---

## 📊 File Structure

```
ocr-text-extractor/
├── frontend/                  # Mobile app
│   ├── app/
│   │   └── index.tsx         # Main screen
│   ├── app.json              # Expo config
│   ├── eas.json              # Build config
│   ├── package.json          # Dependencies
│   └── .env.example          # Environment template
│
├── backend/                   # API server
│   ├── server.py             # FastAPI app
│   ├── requirements.txt      # Python packages
│   └── .env.example          # Environment template
│
├── BUILD_INSTRUCTIONS.md      # Detailed guide
├── README.md                  # This file
├── quickstart.sh              # Setup script (Mac/Linux)
└── quickstart.bat             # Setup script (Windows)
```

---

## ⚙️ Advanced Configuration

### Change App Name:

Edit `frontend/app.json`:
```json
{
  "expo": {
    "name": "Your App Name",
    "slug": "your-app-slug"
  }
}
```

### Change App Icon:

Replace `frontend/assets/images/icon.png` with your 1024x1024 PNG.

### Supported Languages:

The OCR engines support:
- English
- Spanish
- French
- German
- Italian
- Portuguese
- And many more Latin-script languages

Handwriting recognition is limited across all languages.

---

## 📖 Additional Resources

- **Expo Documentation**: https://docs.expo.dev
- **EAS Build Guide**: https://docs.expo.dev/build/introduction/
- **ML Kit Docs**: https://developers.google.com/ml-kit/vision/text-recognition
- **Troubleshooting**: See BUILD_INSTRUCTIONS.md

---

## 💡 Tips for Best Results

### For Better OCR Accuracy:
1. Use good lighting
2. Hold camera steady
3. Ensure text is in focus
4. Avoid shadows and glare
5. Higher contrast is better
6. Works best with printed text

### For PDFs:
- Take screenshots of PDF pages
- Use "Upload Image" feature
- Process one page at a time

### Performance:
- First text extraction may take 2-3 seconds
- Subsequent extractions are faster
- Larger images take longer
- No internet needed after installation

---

## 🚀 Next Steps

After building your app:

1. **Test thoroughly** on your device
2. **Share with friends** (send them the APK/IPA)
3. **Improve** - modify the code as needed
4. **Deploy to stores** (optional) - requires developer accounts

---

## ✨ You're All Set!

Your OCR app is ready to use. It's:
- ✅ Free
- ✅ Offline
- ✅ Private (no data collection)
- ✅ Open source
- ✅ Customizable

**Enjoy extracting text from images!** 📸➡️📝
