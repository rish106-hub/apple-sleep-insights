from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_analysis import generate_insights

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/')
def home():
    return "Hello from Flask!"

@app.route('/upload_sleep_data', methods=['POST'])
def upload_sleep_data():
    sleep_data = request.json  # Receive JSON data
    print("Received sleep data:", sleep_data)  # Log for debugging
    insights = generate_insights(sleep_data)
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True)
