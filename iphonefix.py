import os
import plistlib

def create_info_plist(plist_path):
    """Create a new Info.plist file if it doesn't exist."""
    print(f"🔍 Checking Info.plist at {plist_path}...")
    if os.path.exists(plist_path):
        print(f"✅ Info.plist already exists at {plist_path}.")
        return

    # Create a default Info.plist with required keys
    plist_data = {
        "NSHealthShareUsageDescription": "This app uses HealthKit to analyze your sleep data and provide insights for better sleep health.",
        "NSHealthUpdateUsageDescription": "This app writes data to HealthKit to track and improve your health."
    }

    try:
        with open(plist_path, 'wb') as f:
            plistlib.dump(plist_data, f)
            print(f"✅ Created Info.plist with required keys at {plist_path}.")
    except Exception as e:
        print(f"❌ Error creating Info.plist: {e}")

def fix_info_plist(plist_path):
    """Ensure required keys are present in an existing Info.plist."""
    if not os.path.exists(plist_path):
        create_info_plist(plist_path)
        return

    try:
        with open(plist_path, 'rb') as f:
            plist = plistlib.load(f)

        # Required keys
        required_keys = {
            "NSHealthShareUsageDescription": "This app uses HealthKit to analyze your sleep data and provide insights for better sleep health.",
            "NSHealthUpdateUsageDescription": "This app writes data to HealthKit to track and improve your health."
        }

        # Add missing keys
        for key, value in required_keys.items():
            if key not in plist:
                print(f"❌ Missing key: {key}. Adding it...")
                plist[key] = value

        # Save changes
        with open(plist_path, 'wb') as f:
            plistlib.dump(plist, f)
            print(f"✅ Updated Info.plist with required keys.")

    except Exception as e:
        print(f"❌ Error processing Info.plist: {e}")

def fix_swift_file(file_path):
    """Ensure required imports and attributes are present in Swift files."""
    print(f"🔍 Checking Swift file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            code = f.readlines()

        # Check and fix for `import HealthKit`
        if not any("import HealthKit" in line for line in code):
            print(f"❌ Missing 'import HealthKit' in {file_path}. Adding it...")
            code.insert(0, "import HealthKit\n")

        # Check and fix for `@main` in SleepTrackerApp.swift
        if "SleepTrackerApp.swift" in file_path:
            if not any("@main" in line for line in code):
                print(f"❌ Missing '@main' in {file_path}. Adding it...")
                for i, line in enumerate(code):
                    if line.strip().startswith("struct SleepTrackerApp"):
                        code.insert(i, "@main\n")
                        break

        # Write corrected code back to the file
        with open(file_path, 'w') as f:
            f.writelines(code)
            print(f"✅ Fixed issues in {file_path}.")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

def traverse_and_fix(folder_path):
    """Recursively traverse folders and fix issues."""
    print(f"🔍 Traversing folder: {folder_path}")
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".swift"):
                fix_swift_file(file_path)
            elif file == "Info.plist":
                fix_info_plist(file_path)

def main():
    """Main function to orchestrate fixes."""
    print("🔧 Starting iPhone project fix tool...\n")

    # Define paths
    root_dir = os.getcwd()
    ios_app_dir = os.path.join(root_dir, "ios-app")
    sleep_tracker_dir = os.path.join(ios_app_dir, "Sleeptracker")
    plist_path = os.path.join(sleep_tracker_dir, "Info.plist")

    # Ensure ios-app and Sleeptracker directories exist
    if not os.path.isdir(ios_app_dir):
        print(f"❌ ios-app directory not found: {ios_app_dir}")
        return
    if not os.path.isdir(sleep_tracker_dir):
        print(f"❌ Sleeptracker directory not found: {sleep_tracker_dir}")
        return

    # Check and fix Info.plist
    create_info_plist(plist_path)

    # Traverse directories and fix Swift files
    traverse_and_fix(ios_app_dir)

    print("\n✅ All fixes completed. If there were errors, they have been logged or corrected.")

if __name__ == "__main__":
    main()
