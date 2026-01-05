# fix_compile_options.py
build_gradle_path = "android/app/build.gradle"

with open(build_gradle_path, 'r') as f:
    lines = f.readlines()

# Find where to insert compileOptions (after namespace or compileSdk)
new_lines = []
inserted = False

for i, line in enumerate(lines):
    new_lines.append(line)
    
    # Insert after namespace line
    if 'namespace' in line and not inserted:
        # Check if compileOptions doesn't already exist
        if 'compileOptions' not in ''.join(lines):
            new_lines.append('\n')
            new_lines.append('    compileOptions {\n')
            new_lines.append('        sourceCompatibility JavaVersion.VERSION_11\n')
            new_lines.append('        targetCompatibility JavaVersion.VERSION_11\n')
            new_lines.append('    }\n')
            inserted = True
            print("✅ Added compileOptions")

if inserted:
    with open(build_gradle_path, 'w') as f:
        f.writelines(new_lines)
else:
    print("✅ compileOptions likely already exists or namespace not found")