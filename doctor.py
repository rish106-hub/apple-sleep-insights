#!/usr/bin/env python3
import os
import subprocess
import time
import requests
import sys

# ----- Folder and File Checks -----

def check_folder_structure():
    """Check that the required folders exist."""
    required_folders = ["backend", "frontend", "ios-app"]
    errors = []
    for folder in required_folders:
        if not os.path.isdir(folder):
            errors.append(f"Missing folder: {folder}")
    return errors

def check_files_in_folder(folder, required_files):
    """Check that required files exist in the given folder."""
    errors = []
    for file in required_files:
        path = os.path.join(folder, file)
        if not os.path.isfile(path):
            errors.append(f"Missing file: {path}")
    return errors

def check_backend_files():
    required = ["app.py", "healthkit_api.py", "ai_analysis.py", "requirements.txt"]
    return check_files_in_folder("backend", required)

def check_frontend_files():
    required = ["App.js", "index.js", "App.css", "index.html"]
    return check_files_in_folder("frontend", required)

def check_ios_files():
    required = ["HealthDataManager.swift", "SleepTrackerApp.swift"]
    return check_files_in_folder("ios-app", required)

# ----- Dependency Checks -----

def check_python_packages():
    """Ensure required Python packages are installed."""
    errors = []
    for package in ["flask", "requests"]:
        try:
            subprocess.run(["pip3", "show", package], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            errors.append(f"Python package '{package}' is not installed.")
    return errors

def check_node_modules():
    """Check if 'node_modules' exists in the frontend folder."""
    node_modules_path = os.path.join("frontend", "node_modules")
    if not os.path.isdir(node_modules_path):
        return ["Node modules not installed in 'frontend'. Run 'npm install' inside the frontend folder."]
    return []

def check_frontend_integration():
    """Check that the frontend code references the backend URL."""
    errors = []
    try:
        with open(os.path.join("frontend", "App.js"), "r") as f:
            content = f.read()
            if "http://localhost:5000/upload_sleep_data" not in content:
                errors.append("Frontend integration issue: 'http://localhost:5000/upload_sleep_data' not found in App.js.")
    except Exception as e:
        errors.append(f"Error reading frontend/App.js: {str(e)}")
    return errors

# ----- Backend Integration Test -----

def test_backend_integration():
    """
    Start the Flask backend, send a dummy POST request, and verify the response.
    Returns a tuple (proc, error_message). If no error, error_message is None.
    """
    try:
        proc = subprocess.Popen(
            ["python3", "backend/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        return None, f"Failed to start backend server: {str(e)}"
    
    # Wait for the backend server to start
    time.sleep(2)
    
    try:
        response = requests.post(
            "http://localhost:5000/upload_sleep_data",
            json={"sleep": "dummy sleep data"},
            timeout=5
        )
        if response.status_code != 200:
            return proc, f"Backend test failed: Status code {response.status_code}"
        data = response.json()
        # Check for expected keys and dummy values
        if "sleep_score" not in data or "analysis" not in data:
            return proc, "Backend test failed: Response JSON missing required keys."
        if data.get("sleep_score") != 85:
            return proc, f"Backend test failed: Expected sleep_score 85, got {data.get('sleep_score')}"
    except Exception as e:
        return proc, f"Backend test failed: {str(e)}"
    
    return proc, None

# ----- Main Diagnostic Routine -----

def main():
    overall_errors = []
    
    # 1. Folder structure and files
    overall_errors.extend(check_folder_structure())
    overall_errors.extend(check_backend_files())
    overall_errors.extend(check_frontend_files())
    overall_errors.extend(check_ios_files())
    
    # 2. Dependencies
    overall_errors.extend(check_python_packages())
    overall_errors.extend(check_node_modules())
    
    # 3. Frontend integration check
    overall_errors.extend(check_frontend_integration())
    
    if overall_errors:
        print("Errors detected:")
        for error in overall_errors:
            print(f" - {error}")
        print("Please correct these issues and run doctor.py again.")
        sys.exit(1)
    else:
        print("Folder structure, files, and dependencies: ALL GOOD.")
    
    # 4. Test backend integration
    print("Testing backend integration...")
    proc, backend_error = test_backend_integration()
    if backend_error:
        print(f"Error during backend integration test: {backend_error}")
        if proc:
            proc.terminate()
        sys.exit(1)
    else:
        print("Backend integration test: ALL GOOD.")
    
    # Terminate the backend process after testing
    if proc:
        proc.terminate()
        proc.wait()
    
    print("All diagnostics passed. ALL GOOD.")

if __name__ == "__main__":
    main()
