# OCR Text Extractor - Build Instructions

## Overview
This is a mobile OCR (Optical Character Recognition) app built with Expo and React Native that extracts text from images, PDFs, and camera captures. It works **100% offline** using on-device ML models.

## Features
✅ Camera capture for OCR
✅ Upload images from gallery
✅ PDF support (screenshot pages)
✅ Offline text recognition (Google ML Kit + Apple Vision)
✅ Copy to clipboard
✅ Export as TXT file
✅ Export as DOCX file
✅ No database - no history saved
✅ Works on both Android and iOS

## Important Note about Expo Go
⚠️ **This app CANNOT run in Expo Go** because it uses native modules (`expo-text-extractor`, `expo-image-picker`, etc.) that require a **custom development build**.

You MUST build the app as a standalone native app to use it.

---

## Prerequisites

### For All Platforms:
- Node.js 18 or later
- npm or yarn
- Git

### For Android Build:
- Android Studio
- Java Development Kit (JDK) 17
- Android SDK

### For iOS Build (Mac only):
- Xcode 15 or later
- CocoaPods
- iOS Simulator or physical iPhone

---

## Step 1: Download the Project

### Option A: Clone from this environment
```bash
# Copy the entire /app directory to your local machine
# You can use scp, rsync, or download as zip
```

### Option B: If using Git
```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## Step 2: Install Dependencies

### Backend (Python FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend (Expo/React Native)
```bash
cd frontend
yarn install
# or
npm install
```

---

## Step 3: Build the Mobile App

### Option A: Build for Android (APK)

#### Method 1: Local Build with Expo
```bash
cd frontend

# Install EAS CLI globally
npm install -g eas-cli

# Login to Expo (create free account if needed)
eas login

# Configure the build
eas build:configure

# Build APK (for Android)
eas build --platform android --profile preview

# The build will be done on Expo's servers
# Download the APK when complete and install on your Android device
```

#### Method 2: Local Android Studio Build
```bash
cd frontend

# Generate native Android project
npx expo prebuild --platform android

# Open Android Studio
# File > Open > Select the 'android' folder
# Build > Build Bundle(s) / APK(s) > Build APK(s)
# APK will be in android/app/build/outputs/apk/
```

### Option B: Build for iOS (Mac only)

```bash
cd frontend

# Generate native iOS project
npx expo prebuild --platform ios

# Install CocoaPods dependencies
cd ios
pod install
cd ..

# Open Xcode
open ios/ocrtextextractor.xcworkspace

# In Xcode:
# 1. Select your development team
# 2. Connect your iPhone or select simulator
# 3. Click the Play button to build and run
```

### Option C: Build for Both Platforms (EAS Build)
```bash
cd frontend

# Build for both platforms
eas build --platform all

# Or build just one:
eas build --platform android
eas build --platform ios
```

---

## Step 4: Install on Your Device

### Android:
1. Download the APK file
2. On your Android phone, go to Settings > Security
3. Enable "Install from Unknown Sources"
4. Open the APK file and install

### iOS:
1. Connect your iPhone to your Mac
2. Open Xcode
3. Select your device
4. Click Run
5. Trust the developer profile on your iPhone (Settings > General > VPN & Device Management)

---

## Step 5: Running the Backend (Optional for DOCX export)

The app works **fully offline** for OCR. However, to generate DOCX files, you need the backend running:

### On Your Laptop:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Update Frontend to Connect to Local Backend:
Edit `/frontend/.env`:
```
EXPO_PUBLIC_BACKEND_URL=http://YOUR_LOCAL_IP:8001
```

Replace `YOUR_LOCAL_IP` with your laptop's local IP address (e.g., 192.168.1.100)

To find your local IP:
- **Mac/Linux**: `ifconfig | grep "inet "`
- **Windows**: `ipconfig`

---

## How to Use the App

1. **Launch the app** on your mobile device
2. **Choose input method**:
   - Take Photo (camera)
   - Upload Image (gallery)
   - Upload PDF
3. **View extracted text** - Text will appear automatically
4. **Export options**:
   - Copy to clipboard
   - Download as TXT
   - Download as DOCX (requires backend)

---

## Troubleshooting

### Build Errors

**Issue**: "expo-text-extractor requires native code"
- **Solution**: Use `eas build` or `npx expo prebuild` - don't use Expo Go

**Issue**: "Failed to build Android"
- **Solution**: Make sure Android Studio and JDK 17 are installed

**Issue**: "Pod install failed" (iOS)
- **Solution**: Run `cd ios && pod install --repo-update`

### Runtime Errors

**Issue**: "Camera permission denied"
- **Solution**: Go to Settings > Apps > OCR Text Extractor > Permissions > Enable Camera

**Issue**: "Text extraction not supported"
- **Solution**: Make sure you built a development build, not using Expo Go

**Issue**: "DOCX generation failed"
- **Solution**: Make sure backend is running and EXPO_PUBLIC_BACKEND_URL is correct

---

## File Structure

```
app/
├── backend/
│   ├── server.py          # FastAPI backend
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── app/
│   │   └── index.tsx      # Main app screen
│   ├── app.json           # Expo configuration
│   ├── package.json       # JavaScript dependencies
│   └── .env               # Environment variables
└── BUILD_INSTRUCTIONS.md  # This file
```

---

## Technologies Used

- **Frontend**: Expo, React Native, TypeScript
- **OCR Engine**: Google ML Kit (Android), Apple Vision (iOS)
- **Backend**: Python FastAPI
- **DOCX Generation**: python-docx

---

## Offline Capability

✅ **Fully Offline**:
- Text extraction from images
- Camera capture
- Gallery selection
- Copy to clipboard
- TXT file export

⚠️ **Requires Internet Once** (for build only):
- Initial app build
- Installing on device

❌ **Requires Local Backend**:
- DOCX file generation (backend must be running on your laptop)

---

## App Size

- **Android APK**: ~40-50 MB (includes ML Kit models)
- **iOS IPA**: ~35-45 MB (includes Vision framework)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error logs
3. Ensure all prerequisites are installed

---

## License

Free to use for personal and commercial projects.
