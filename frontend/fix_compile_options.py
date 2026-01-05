import json
import os
import subprocess

# 1. Manually inject the dependency into package.json to avoid npm logic errors
with open('package.json', 'r') as f:
    pkg = json.load(f)

pkg['dependencies']['expo-text-extractor'] = "^0.2.2"

with open('package.json', 'w') as f:
    json.dump(pkg, f, indent=2)

print("✅ Manually updated package.json with expo-text-extractor")

# 2. Run install with the bypass flag
print("⏳ Running forced install...")
subprocess.run("npm install --legacy-peer-deps", shell=True)

# 3. Clean and Build
print("🚀 Starting EAS Build...")
subprocess.run("npx eas-cli build --platform android --profile preview", shell=True)