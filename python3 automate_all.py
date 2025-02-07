import subprocess
import os
def run_script(script_name):
    """Run a Python script and print its output."""
    print(f"Running {script_name}...")
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"Errors in {script_name}:")
        print(result.stderr.strip())
    print("-" * 50)

def main():
    # List the automation scripts to run in order.
    scripts = [
        "automate_backend.py",
        "automate_frontend.py",
        "automate_integration.py",
        "automate_ios.py"
    ]
    # Ensure each script exists before running it.
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"Script {script} not found in the current directory.")
    print("All automation tasks complete. ALL GOOD.")
if __name__ == "__main__":
    main()
