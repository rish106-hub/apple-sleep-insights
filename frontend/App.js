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