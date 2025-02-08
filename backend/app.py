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
