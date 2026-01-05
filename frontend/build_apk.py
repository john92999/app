#!/usr/bin/env python3
"""
React Native APK Builder - Complete Solution
Fixes dependency issues and builds APK for Android
"""

import os
import subprocess
import shutil
import sys
import platform
from pathlib import Path
import json

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class APKBuilder:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.is_windows = platform.system() == 'Windows'
        self.steps_completed = []
        self.steps_failed = []
        
    def print_header(self, text):
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}{Colors.END}\n")
    
    def print_success(self, text):
        print(f"{Colors.GREEN}✓ {text}{Colors.END}")
    
    def print_error(self, text):
        print(f"{Colors.RED}✗ {text}{Colors.END}")
    
    def print_info(self, text):
        print(f"{Colors.BLUE}ℹ {text}{Colors.END}")
    
    def print_warning(self, text):
        print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")
    
    def run_command(self, command, step_name, shell=True, check_exit=True):
        """Run a command and handle errors"""
        self.print_info(f"Running: {command}")
        try:
            if self.is_windows and not shell:
                # For Windows, we need to handle commands differently
                result = subprocess.run(
                    command,
                    shell=True,
                    check=check_exit,
                    capture_output=False,
                    text=True
                )
            else:
                result = subprocess.run(
                    command,
                    shell=shell,
                    check=check_exit,
                    capture_output=False,
                    text=True
                )
            
            self.steps_completed.append(step_name)
            self.print_success(f"{step_name} completed")
            return True
            
        except subprocess.CalledProcessError as e:
            self.steps_failed.append(step_name)
            self.print_error(f"{step_name} failed")
            return False
        except Exception as e:
            self.steps_failed.append(step_name)
            self.print_error(f"{step_name} error: {str(e)}")
            return False
    
    def check_prerequisites(self):
        """Check if required tools are installed"""
        self.print_header("CHECKING PREREQUISITES")
        
        prerequisites = {
            'Node.js': 'node --version',
            'npm': 'npm --version',
            'Git': 'git --version'
        }
        
        all_good = True
        for tool, command in prerequisites.items():
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                version = result.stdout.strip()
                self.print_success(f"{tool} is installed: {version}")
            except:
                self.print_error(f"{tool} is NOT installed")
                all_good = False
        
        if not all_good:
            self.print_warning("Please install missing prerequisites")
            return False
        return True
    
    def backup_package_json(self):
        """Backup package.json"""
        self.print_header("STEP 1/8: BACKING UP PACKAGE.JSON")
        
        package_json = self.project_dir / "package.json"
        backup_file = self.project_dir / "package.json.backup"
        
        if package_json.exists():
            shutil.copy2(package_json, backup_file)
            self.print_success(f"Backed up to: {backup_file}")
            return True
        else:
            self.print_error("package.json not found!")
            return False
    
    def downgrade_react_native(self):
        """Downgrade React Native to stable version"""
        self.print_header("STEP 2/8: DOWNGRADING REACT NATIVE TO 0.74.5")
        self.print_info("This is the most stable version for Expo...")
        
        return self.run_command(
            "npm install react-native@0.74.5",
            "React Native downgrade"
        )
    
    def remove_node_modules(self):
        """Remove node_modules folder"""
        self.print_header("STEP 3/8: CLEANING NODE_MODULES")
        
        node_modules = self.project_dir / "node_modules"
        if node_modules.exists():
            self.print_info("Removing node_modules folder...")
            try:
                shutil.rmtree(node_modules)
                self.print_success("node_modules removed")
                return True
            except Exception as e:
                self.print_error(f"Failed to remove node_modules: {e}")
                return False
        else:
            self.print_warning("node_modules not found, skipping...")
            return True
    
    def reinstall_dependencies(self):
        """Reinstall all dependencies"""
        self.print_header("STEP 4/8: REINSTALLING DEPENDENCIES")
        self.print_info("This may take several minutes...")
        
        return self.run_command(
            "npm install --legacy-peer-deps",
            "Dependencies installation"
        )
    
    def clean_android_folder(self):
        """Clean Android build folder"""
        self.print_header("STEP 5/8: CLEANING ANDROID BUILD")
        
        android_dir = self.project_dir / "android"
        if android_dir.exists():
            build_dir = android_dir / "app" / "build"
            if build_dir.exists():
                self.print_info("Removing Android build folder...")
                try:
                    shutil.rmtree(build_dir)
                    self.print_success("Android build cleaned")
                except Exception as e:
                    self.print_warning(f"Could not clean build: {e}")
            return True
        else:
            self.print_info("Android folder not found, will be created by prebuild")
            return True
    
    def rebuild_android(self):
        """Rebuild Android folder with Expo"""
        self.print_header("STEP 6/8: REBUILDING ANDROID FOLDER")
        self.print_info("Using Expo prebuild...")
        
        return self.run_command(
            "npx expo prebuild --clean --platform android",
            "Android rebuild"
        )
    
    def update_gradle_wrapper(self):
        """Update Gradle wrapper to compatible version"""
        self.print_header("STEP 7/8: UPDATING GRADLE WRAPPER")
        
        android_dir = self.project_dir / "android"
        if not android_dir.exists():
            self.print_error("Android directory not found!")
            return False
        
        gradle_wrapper_props = android_dir / "gradle" / "wrapper" / "gradle-wrapper.properties"
        gradle_wrapper_props.parent.mkdir(parents=True, exist_ok=True)
        
        # Write Gradle 8.3 configuration
        gradle_config = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.3-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
        
        try:
            with open(gradle_wrapper_props, 'w') as f:
                f.write(gradle_config)
            self.print_success("Gradle wrapper updated to 8.3")
            return True
        except Exception as e:
            self.print_error(f"Failed to update Gradle wrapper: {e}")
            return False
    
    def build_apk(self):
        """Build the APK"""
        self.print_header("STEP 8/8: BUILDING APK")
        self.print_info("This will take several minutes...")
        self.print_warning("First build downloads Gradle dependencies...")
        
        android_dir = self.project_dir / "android"
        
        # Change to android directory
        os.chdir(android_dir)
        
        # Run Gradle commands
        gradlew = "./gradlew" if not self.is_windows else "gradlew.bat"
        
        # Clean first
        self.print_info("Cleaning Gradle cache...")
        self.run_command(f"{gradlew} clean", "Gradle clean", check_exit=False)
        
        # Build debug APK
        self.print_info("Building debug APK...")
        success = self.run_command(
            f"{gradlew} assembleDebug",
            "APK build"
        )
        
        # Change back to project directory
        os.chdir(self.project_dir)
        
        return success
    
    def find_apk(self):
        """Find and display APK location"""
        self.print_header("FINDING APK FILE")
        
        apk_path = self.project_dir / "android" / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
        
        if apk_path.exists():
            size_mb = apk_path.stat().st_size / (1024 * 1024)
            self.print_success(f"APK built successfully!")
            print(f"\n{Colors.GREEN}{Colors.BOLD}APK Location:{Colors.END}")
            print(f"{Colors.BLUE}{apk_path.absolute()}{Colors.END}")
            print(f"{Colors.YELLOW}Size: {size_mb:.2f} MB{Colors.END}\n")
            return True
        else:
            self.print_error("APK file not found!")
            self.print_info("Check the build logs above for errors")
            return False
    
    def print_summary(self):
        """Print build summary"""
        self.print_header("BUILD SUMMARY")
        
        print(f"{Colors.GREEN}Completed Steps:{Colors.END}")
        for step in self.steps_completed:
            print(f"  ✓ {step}")
        
        if self.steps_failed:
            print(f"\n{Colors.RED}Failed Steps:{Colors.END}")
            for step in self.steps_failed:
                print(f"  ✗ {step}")
        
        print(f"\n{Colors.BLUE}Total: {len(self.steps_completed)}/{len(self.steps_completed) + len(self.steps_failed)} steps successful{Colors.END}")
    
    def install_instructions(self):
        """Show installation instructions"""
        self.print_header("INSTALLATION INSTRUCTIONS")
        
        print(f"{Colors.BLUE}To install on your Android device:{Colors.END}\n")
        print("1. Transfer the APK to your phone (USB, email, cloud)")
        print("2. Enable 'Install from Unknown Sources' in Settings")
        print("3. Open the APK file and tap Install")
        print(f"\n{Colors.YELLOW}Note: This is a debug build for testing{Colors.END}")
    
    def run(self):
        """Run the complete build process"""
        self.print_header("REACT NATIVE APK BUILDER")
        print(f"Working Directory: {self.project_dir}")
        print(f"Platform: {platform.system()}")
        
        input(f"\n{Colors.YELLOW}Press Enter to start the build process...{Colors.END}")
        
        # Check prerequisites
        if not self.check_prerequisites():
            self.print_error("Please install missing prerequisites and try again")
            return False
        
        # Run all build steps
        steps = [
            self.backup_package_json,
            self.downgrade_react_native,
            self.remove_node_modules,
            self.reinstall_dependencies,
            self.clean_android_folder,
            self.rebuild_android,
            self.update_gradle_wrapper,
            self.build_apk,
        ]
        
        for step in steps:
            if not step():
                self.print_error(f"Build process stopped due to failure")
                choice = input(f"\n{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower()
                if choice != 'y':
                    break
        
        # Find APK
        self.find_apk()
        
        # Print summary
        self.print_summary()
        
        # Installation instructions
        self.install_instructions()
        
        return len(self.steps_failed) == 0

def main():
    builder = APKBuilder()
    success = builder.run()
    
    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Build completed successfully!{Colors.END}")
        sys.exit(0)
    else:
        print(f"\n{Colors.YELLOW}⚠ Build completed with some errors{Colors.END}")
        print(f"{Colors.BLUE}Check the logs above for details{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()