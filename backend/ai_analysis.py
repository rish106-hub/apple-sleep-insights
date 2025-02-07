import requests

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
