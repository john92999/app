#!/usr/bin/env python3
"""
Downgrade React Native to 0.74.5 and Build APK
Automates the entire process of fixing version issues and building the app
"""

import os
import subprocess
import shutil
import sys
from pathlib import Path

class APKBuilder:
    def __init__(self, frontend_path):
        self.frontend_path = Path(frontend_path)
        self.steps_completed = []
        self.current_step = 0
        self.total_steps = 6

    def print_header(self, message):
        """Print a formatted header"""
        print("\n" + "=" * 70)
        print(f"  STEP {self.current_step}/{self.total_steps}: {message}")
        print("=" * 70)

    def run_command(self, command, cwd=None, shell=True):
        """Run a shell command and handle errors"""
        if cwd is None:
            cwd = self.frontend_path
        
        print(f"\n▶ Running: {command}")
        print(f"  Directory: {cwd}")
        
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                shell=shell,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Command failed with error:")
            print(e.stdout)
            return False

    def backup_package_json(self):
        """Backup package.json"""
        self.current_step += 1
        self.print_header("Backing up package.json")
        
        package_json = self.frontend_path / "package.json"
        backup_path = self.frontend_path / "package.json.bak"
        
        try:
            shutil.copy2(package_json, backup_path)
            print(f"✅ Backed up to: {backup_path}")
            self.steps_completed.append("Backup package.json")
            return True
        except Exception as e:
            print(f"❌ Failed to backup: {e}")
            return False

    def downgrade_react_native(self):
        """Downgrade React Native to 0.74.5"""
        self.current_step += 1
        self.print_header("Downgrading React Native to 0.74.5")
        
        success = self.run_command("npm install react-native@0.74.5")
        
        if success:
            print("✅ React Native downgraded to 0.74.5")
            self.steps_completed.append("Downgrade React Native")
        else:
            print("❌ Failed to downgrade React Native")
        
        return success

    def remove_node_modules(self):
        """Remove node_modules directory"""
        self.current_step += 1
        self.print_header("Removing node_modules")
        
        node_modules = self.frontend_path / "node_modules"
        
        try:
            if node_modules.exists():
                print(f"Deleting: {node_modules}")
                shutil.rmtree(node_modules)
                print("✅ node_modules removed")
            else:
                print("ℹ️  node_modules doesn't exist, skipping")
            
            self.steps_completed.append("Remove node_modules")
            return True
        except Exception as e:
            print(f"❌ Failed to remove node_modules: {e}")
            return False

    def reinstall_dependencies(self):
        """Reinstall npm dependencies"""
        self.current_step += 1
        self.print_header("Reinstalling dependencies")
        
        print("This may take a few minutes...")
        success = self.run_command("npm install")
        
        if success:
            print("✅ Dependencies reinstalled")
            self.steps_completed.append("Reinstall dependencies")
        else:
            print("❌ Failed to reinstall dependencies")
        
        return success

    def rebuild_android(self):
        """Rebuild Android folder using expo prebuild"""
        self.current_step += 1
        self.print_header("Rebuilding Android folder")
        
        success = self.run_command("npx expo prebuild --clean --platform android")
        
        if success:
            print("✅ Android folder rebuilt")
            self.steps_completed.append("Rebuild Android folder")
        else:
            print("❌ Failed to rebuild Android folder")
        
        return success

    def build_apk(self):
        """Build the APK"""
        self.current_step += 1
        self.print_header("Building APK")
        
        android_path = self.frontend_path / "android"
        
        if not android_path.exists():
            print(f"❌ Android directory not found: {android_path}")
            return False
        
        # Clean first
        print("\n🧹 Cleaning previous builds...")
        clean_success = self.run_command("./gradlew clean", cwd=android_path)
        
        if not clean_success:
            print("⚠️  Clean failed, but continuing with build...")
        
        # Build debug APK
        print("\n🔨 Building debug APK...")
        build_success = self.run_command("./gradlew assembleDebug", cwd=android_path)
        
        if build_success:
            print("✅ APK built successfully!")
            self.steps_completed.append("Build APK")
            
            # Find and show APK location
            apk_path = android_path / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
            if apk_path.exists():
                print(f"\n🎉 APK Location: {apk_path}")
                print(f"   Size: {apk_path.stat().st_size / (1024*1024):.2f} MB")
            else:
                print("\n⚠️  Build succeeded but APK not found at expected location")
        else:
            print("❌ Failed to build APK")
        
        return build_success

    def print_summary(self):
        """Print summary of operations"""
        print("\n" + "=" * 70)
        print("  BUILD SUMMARY")
        print("=" * 70)
        
        print(f"\n✅ Steps completed ({len(self.steps_completed)}/{self.total_steps}):")
        for step in self.steps_completed:
            print(f"   ✓ {step}")
        
        failed_steps = self.total_steps - len(self.steps_completed)
        if failed_steps > 0:
            print(f"\n❌ Steps failed: {failed_steps}")
        
        print("\n" + "=" * 70)
        
        if len(self.steps_completed) == self.total_steps:
            print("🎉 SUCCESS! Your APK is ready!")
            apk_path = self.frontend_path / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
            print(f"\n📱 APK Location:")
            print(f"   {apk_path}")
            print(f"\n📲 Next steps:")
            print(f"   1. Copy the APK to your phone")
            print(f"   2. Enable 'Install from Unknown Sources' on your phone")
            print(f"   3. Install the APK")
        else:
            print("⚠️  Some steps failed. Check the errors above.")
            print("\n💡 Troubleshooting:")
            print("   1. Make sure you're in the frontend directory")
            print("   2. Check your internet connection")
            print("   3. Try running individual commands manually")
        
        print("=" * 70)

    def run(self):
        """Run all build steps"""
        print("\n" + "=" * 70)
        print("  REACT NATIVE APK BUILDER")
        print("  Downgrade to 0.74.5 and Build")
        print("=" * 70)
        print(f"\nWorking directory: {self.frontend_path}")
        print(f"Total steps: {self.total_steps}")
        
        input("\nPress Enter to continue...")
        
        # Execute all steps
        steps = [
            self.backup_package_json,
            self.downgrade_react_native,
            self.remove_node_modules,
            self.reinstall_dependencies,
            self.rebuild_android,
            self.build_apk
        ]
        
        for step_func in steps:
            if not step_func():
                print(f"\n⚠️  Step failed. Do you want to continue? (y/n)")
                response = input().strip().lower()
                if response != 'y':
                    print("\n🛑 Build process stopped by user.")
                    break
        
        # Print summary
        self.print_summary()

def main():
    # Detect if we're in the right directory
    current_dir = Path.cwd()
    
    # Check if we're in frontend directory
    if not (current_dir / "package.json").exists():
        print("❌ Error: package.json not found!")
        print(f"   Current directory: {current_dir}")
        print("\n💡 Please run this script from your frontend directory:")
        print("   cd /d/app/frontend")
        print("   python build_apk.py")
        sys.exit(1)
    
    if not (current_dir / "android").exists():
        print("⚠️  Warning: android directory not found")
        print("   It will be created during the build process")
    
    # Create builder and run
    builder = APKBuilder(current_dir)
    builder.run()

if __name__ == "__main__":
    main()