#!/usr/bin/env python3
"""
Comprehensive Gradle Build Fixer for React Native/Expo Projects
Fixes common Kotlin and Java toolchain issues
"""

import os
import re
import shutil
from pathlib import Path

class GradleFixer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.fixes_applied = []
        self.errors = []

    def log(self, message, is_error=False):
        """Log messages"""
        prefix = "❌ ERROR:" if is_error else "✅"
        print(f"{prefix} {message}")
        if is_error:
            self.errors.append(message)
        else:
            self.fixes_applied.append(message)

    def backup_file(self, file_path):
        """Create backup of file before modifying"""
        backup_path = f"{file_path}.backup"
        if not os.path.exists(backup_path):
            shutil.copy2(file_path, backup_path)
            self.log(f"Created backup: {backup_path}")

    def fix_kotlin_build_files(self):
        """Fix allWarningsAsErrors issues in Kotlin build files"""
        self.log("\n=== Fixing Kotlin Build Files ===")
        
        gradle_plugin_path = self.project_root / "node_modules" / "@react-native" / "gradle-plugin"
        
        if not gradle_plugin_path.exists():
            self.log(f"Gradle plugin path not found: {gradle_plugin_path}", is_error=True)
            return

        # Find all build.gradle.kts files
        kotlin_files = list(gradle_plugin_path.rglob("build.gradle.kts"))
        
        for file_path in kotlin_files:
            try:
                self.log(f"Checking: {file_path.relative_to(self.project_root)}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file needs fixing
                if 'allWarningsAsErrors =' not in content:
                    self.log(f"  No fix needed")
                    continue
                
                # Backup before modifying
                self.backup_file(file_path)
                
                # Fix the pattern
                pattern = r'(\s+)allWarningsAsErrors\s*=\s*\n\s+project\.properties\["enableWarningsAsErrors"\]\?\.toString\(\)\?\.toBoolean\(\)\s*\?\:\s*false\)?'
                replacement = r'\1allWarningsAsErrors.set(\n\1    project.properties["enableWarningsAsErrors"]?.toString()?.toBoolean() ?: false\n\1)'
                
                new_content = re.sub(pattern, replacement, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    self.log(f"  Fixed allWarningsAsErrors pattern")
                
            except Exception as e:
                self.log(f"  Failed to fix {file_path}: {e}", is_error=True)

    def fix_gradle_properties(self):
        """Update gradle.properties with necessary configurations"""
        self.log("\n=== Updating gradle.properties ===")
        
        gradle_props_path = self.project_root / "android" / "gradle.properties"
        
        if not gradle_props_path.exists():
            self.log(f"gradle.properties not found: {gradle_props_path}", is_error=True)
            return
        
        self.backup_file(gradle_props_path)
        
        with open(gradle_props_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Properties to add/ensure
        properties_to_add = {
            'org.gradle.java.installations.auto-detect': 'false',
            'org.gradle.java.installations.auto-download': 'false',
            'org.gradle.jvmargs': '-Xmx2048m -XX:MaxMetaspaceSize=512m',
            'android.useAndroidX': 'true',
            'android.enableJetifier': 'true',
        }
        
        modified = False
        for key, value in properties_to_add.items():
            if key not in content:
                content += f"\n{key}={value}"
                modified = True
                self.log(f"  Added: {key}={value}")
            else:
                self.log(f"  Already present: {key}")
        
        if modified:
            with open(gradle_props_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def fix_root_build_gradle(self):
        """Fix root build.gradle file"""
        self.log("\n=== Fixing Root build.gradle ===")
        
        build_gradle_path = self.project_root / "android" / "build.gradle"
        
        if not build_gradle_path.exists():
            self.log(f"build.gradle not found: {build_gradle_path}", is_error=True)
            return
        
        self.backup_file(build_gradle_path)
        
        with open(build_gradle_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove problematic sourceCompatibility/targetCompatibility at project level
        lines = content.split('\n')
        new_lines = []
        in_buildscript = False
        in_allprojects = False
        
        for line in lines:
            # Track context
            if 'buildscript' in line and '{' in line:
                in_buildscript = True
            elif 'allprojects' in line and '{' in line:
                in_allprojects = True
            
            # Remove sourceCompatibility/targetCompatibility at root level
            if not in_buildscript and not in_allprojects:
                if re.match(r'\s*(source|target)Compatibility', line):
                    self.log(f"  Removed: {line.strip()}")
                    continue
            
            new_lines.append(line)
            
            if '}' in line:
                if in_buildscript:
                    in_buildscript = False
                if in_allprojects:
                    in_allprojects = False
        
        new_content = '\n'.join(new_lines)
        
        if new_content != content:
            with open(build_gradle_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.log(f"  Updated root build.gradle")

    def fix_app_build_gradle(self):
        """Ensure app/build.gradle has correct Java compatibility settings"""
        self.log("\n=== Checking App build.gradle ===")
        
        app_build_gradle_path = self.project_root / "android" / "app" / "build.gradle"
        
        if not app_build_gradle_path.exists():
            self.log(f"app/build.gradle not found: {app_build_gradle_path}", is_error=True)
            return
        
        with open(app_build_gradle_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if compileOptions exists
        if 'compileOptions' not in content:
            self.log(f"  compileOptions not found - may need manual configuration", is_error=True)
        else:
            self.log(f"  compileOptions present")
        
        # Check if it has proper Java version
        if 'JavaVersion.VERSION_11' in content or 'JavaVersion.VERSION_17' in content:
            self.log(f"  Java version configured")
        else:
            self.log(f"  Java version may need configuration", is_error=True)

    def verify_gradle_wrapper(self):
        """Verify Gradle wrapper version"""
        self.log("\n=== Checking Gradle Wrapper ===")
        
        wrapper_props_path = self.project_root / "android" / "gradle" / "wrapper" / "gradle-wrapper.properties"
        
        if not wrapper_props_path.exists():
            self.log(f"gradle-wrapper.properties not found", is_error=True)
            return
        
        with open(wrapper_props_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Gradle version
        version_match = re.search(r'gradle-(\d+\.\d+(?:\.\d+)?)', content)
        if version_match:
            version = version_match.group(1)
            self.log(f"  Using Gradle version: {version}")
            
            # Recommend stable version
            major_version = int(version.split('.')[0])
            if major_version < 7:
                self.log(f"  Consider upgrading to Gradle 7.6.3 or 8.3", is_error=True)
        else:
            self.log(f"  Could not determine Gradle version", is_error=True)

    def run_all_fixes(self):
        """Run all fixes"""
        print("=" * 60)
        print("  GRADLE BUILD FIXER FOR REACT NATIVE/EXPO")
        print("=" * 60)
        print(f"Project root: {self.project_root}")
        
        try:
            self.fix_kotlin_build_files()
            self.fix_gradle_properties()
            self.fix_root_build_gradle()
            self.fix_app_build_gradle()
            self.verify_gradle_wrapper()
            
            print("\n" + "=" * 60)
            print("  SUMMARY")
            print("=" * 60)
            print(f"✅ Fixes applied: {len(self.fixes_applied)}")
            print(f"❌ Errors encountered: {len(self.errors)}")
            
            if self.errors:
                print("\nErrors that need manual attention:")
                for error in self.errors:
                    print(f"  - {error}")
            
            print("\n" + "=" * 60)
            print("Next steps:")
            print("1. Review the changes")
            print("2. Run: cd android && ./gradlew clean")
            print("3. Run: ./gradlew assembleDebug")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()

def main():
    # Assuming script is run from frontend directory
    current_dir = os.getcwd()
    
    # Check if we're in the right directory
    if not os.path.exists(os.path.join(current_dir, 'android')):
        print("❌ Error: 'android' directory not found!")
        print("Please run this script from your frontend directory (D:/app/frontend)")
        return
    
    fixer = GradleFixer(current_dir)
    fixer.run_all_fixes()

if __name__ == "__main__":
    main()