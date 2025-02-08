import os
import subprocess

# Define backend folder structure
BACKEND_STRUCTURE = {
    "backend": [
        "uploads",  # Directory for uploaded sleep data
        "parsers",  # Data parsing logic
        "tests"  # Unit tests
    ]
}

# Backend files content
APP_PY = """\
from flask import Flask, request, jsonify
import os
import zipfile
from parsers.sleep_parser import parse_sleep_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".zip"):
        return jsonify({"error": "Invalid file format"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(UPLOAD_FOLDER)

        xml_file = os.path.join(UPLOAD_FOLDER, "export.xml")
        insights = parse_sleep_data(xml_file)
        return jsonify(insights), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
"""

SLEEP_PARSER_PY = """\
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_sleep_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sleep_data = []

    for record in root.findall("Record"):
        if record.get("type") == "HKCategoryTypeIdentifierSleepAnalysis":
            sleep_data.append({
                "start": record.get("startDate"),
                "end": record.get("endDate"),
                "value": record.get("value"),
            })

    durations = [
        {
            "date": entry["start"].split("T")[0],
            "duration": calculate_duration(entry["start"], entry["end"]),
        }
        for entry in sleep_data
    ]
    
    return {
        "summary": f"Processed {len(durations)} sleep records.",
        "durations": [entry["duration"] for entry in durations],
        "dates": [entry["date"] for entry in durations],
    }

def calculate_duration(start, end):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    return round((end_dt - start_dt).total_seconds() / 3600, 2)
"""

REQUIREMENTS_TXT = """\
flask
xml.etree.ElementTree
"""

TEST_PARSER_PY = """\
import unittest
from parsers.sleep_parser import parse_sleep_data

class TestSleepParser(unittest.TestCase):
    def test_parse_sleep_data(self):
        sample_xml = '''
        <HealthData>
            <Record type="HKCategoryTypeIdentifierSleepAnalysis" startDate="2025-02-01T23:00:00" endDate="2025-02-02T07:00:00" value="Asleep"/>
        </HealthData>
        '''
        with open("test_export.xml", "w") as f:
            f.write(sample_xml)
        
        result = parse_sleep_data("test_export.xml")
        self.assertEqual(len(result["durations"]), 1)
        self.assertEqual(result["durations"][0], 8.0)

if __name__ == "__main__":
    unittest.main()
"""

# Function to create backend folder structure
def create_backend_structure():
    for folder, subfolders in BACKEND_STRUCTURE.items():
        os.makedirs(folder, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder, subfolder), exist_ok=True)
    print("✅ Backend folder structure created.")

# Function to create necessary backend files
def create_backend_files():
    backend_path = "backend"

    files = {
        os.path.join(backend_path, "app.py"): APP_PY,
        os.path.join(backend_path, "requirements.txt"): REQUIREMENTS_TXT,
        os.path.join(backend_path, "parsers/sleep_parser.py"): SLEEP_PARSER_PY,
        os.path.join(backend_path, "tests/test_parser.py"): TEST_PARSER_PY,
    }

    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)

    print("✅ Backend files created.")

# Function to install dependencies
def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.run(["pip3", "install", "-r", "backend/requirements.txt"])
    print("✅ Dependencies installed.")

# Main function
def main():
    print("🔧 Setting up backend...")
    create_backend_structure()
    create_backend_files()
    install_dependencies()
    print("\n✅ Backend setup complete. You can now run the backend using:")
    print("   cd backend && python3 app.py")

if __name__ == "__main__":
    main()
