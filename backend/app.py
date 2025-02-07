from flask import Flask, request, jsonify
from ai_analysis import generate_insights

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

@app.route('/upload_sleep_data', methods=['POST'])
def upload_sleep_data():
    sleep_data = request.json  # Expecting sleep data in JSON format.
    insights = generate_insights(sleep_data)
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True)
