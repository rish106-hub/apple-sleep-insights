import os

def write_file(filepath, content):
    """Write content to a file at the given filepath."""
    with open(filepath, "w") as f:
        f.write(content)

def main():
    # Assume current working directory is the project root: apple-sleep-insights
    current_dir = os.getcwd()
    frontend_dir = os.path.join(current_dir, "frontend")
    app_js_path = os.path.join(frontend_dir, "App.js")
    
    # New content for App.js to integrate frontend with the backend API
    integration_content = """
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    // Dummy sleep data to simulate real data from Apple Health
    const sleepData = {
      sleep: "dummy sleep data"
    };

    // Send sleep data to the Flask backend endpoint
    fetch('http://localhost:5000/upload_sleep_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sleepData)
    })
      .then(response => response.json())
      .then(data => {
        setInsights(data);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Sleep Insights</h1>
      </header>
      <main className="app-main">
        <p>Welcome to your personalized sleep analytics dashboard.</p>
        <p>Your AI-powered insights will appear here soon.</p>
        {insights && (
          <div>
            <h2>Your Sleep Score: {insights.sleep_score}</h2>
            <p>{insights.analysis}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
""".strip()

    write_file(app_js_path, integration_content)
    print("Integration complete. ALL GOOD.")

if __name__ == "__main__":
    main()
