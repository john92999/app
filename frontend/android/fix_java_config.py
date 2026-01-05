# fix_java_config.py
build_gradle = "build.gradle"

with open(build_gradle, 'r') as f:
    content = f.read()

# Add configuration after allprojects block
insertion_point = content.find('apply plugin: "expo-root-project"')

if insertion_point == -1:
    print("❌ Could not find insertion point")
else:
    # Add subprojects configuration
    config_to_add = '''
subprojects {
    afterEvaluate { project ->
        if (project.hasProperty("android")) {
            android {
                compileOptions {
                    sourceCompatibility JavaVersion.VERSION_11
                    targetCompatibility JavaVersion.VERSION_11
                }
            }
        }
    }
}

'''
    
    new_content = content[:insertion_point] + config_to_add + content[insertion_point:]
    
    with open(build_gradle, 'w') as f:
        f.write(new_content)
    
    print("✅ Added subprojects configuration")