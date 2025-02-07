import os

def write_file(filepath, content):
    """Write content to a file located at filepath."""
    with open(filepath, "w") as f:
        f.write(content)

def main():
    # Assume the current working directory is the project root: apple-sleep-insights
    current_dir = os.getcwd()
    backend_dir = os.path.join(current_dir, "backend")
    
    if not os.path.isdir(backend_dir):
        print("Backend folder not found. Make sure you are in the 'apple-sleep-insights' directory.")
        return

    # Define the contents for each backend file:

    # app.py: Sets up the basic Flask server and an endpoint to process sleep data.
    app_py = '''from flask import Flask, request, jsonify
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
'''

    # healthkit_api.py: Placeholder for functions that will eventually handle Apple HealthKit integration.
    healthkit_api_py = '''# healthkit_api.py
def fetch_sleep_data():
    """
    Placeholder function for Apple HealthKit data retrieval.
    In a real app, this function would interface with an iOS app to get the data.
    """
    return {"sleep": "data"}
'''

    # ai_analysis.py: Contains the AI logic (using a free generative API) to generate sleep insights.
    ai_analysis_py = '''import requests

def generate_insights(sleep_data):
    """
    Generates AI-powered insights from the provided sleep data.
    For now, this returns a dummy insight. Later, you can integrate a free generative AI API.
    """
    prompt = f"Analyze the following sleep data: {sleep_data}"
    
    # Dummy response simulating AI analysis:
    insights = {
        "sleep_score": 85,
        "analysis": "Your sleep data indicates a consistent sleep pattern with room for improvement in deep sleep."
    }
    
    # To integrate a real API, you might do something like:
    # response = requests.post("https://api.example.com/generate", json={"prompt": prompt})
    # insights = response.json()
    
    return insights
'''

    # requirements.txt: Lists the Python packages required for the backend.
    requirements_txt = '''flask
requests
'''

    # Write the files into the backend folder:
    write_file(os.path.join(backend_dir, "app.py"), app_py)
    write_file(os.path.join(backend_dir, "healthkit_api.py"), healthkit_api_py)
    write_file(os.path.join(backend_dir, "ai_analysis.py"), ai_analysis_py)
    write_file(os.path.join(backend_dir, "requirements.txt"), requirements_txt)

    print("Backend setup complete. ALL GOOD.")

if __name__ == "__main__":
    main()
