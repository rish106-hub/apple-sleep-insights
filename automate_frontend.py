import os

def write_file(filepath, content):
    """Write content to a file at the given filepath."""
    with open(filepath, "w") as f:
        f.write(content)

def main():
    # Assume the current working directory is the project root: apple-sleep-insights
    current_dir = os.getcwd()
    frontend_dir = os.path.join(current_dir, "frontend")
    
    if not os.path.isdir(frontend_dir):
        print("Frontend folder not found. Make sure you are in the 'apple-sleep-insights' directory.")
        return

    # Define the content for each frontend file:

    # App.js: Main React component with an Apple-inspired UI
    app_js_content = """import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Sleep Insights</h1>
      </header>
      <main className="app-main">
        <p>Welcome to your personalized sleep analytics dashboard.</p>
        <p>Your AI-powered insights will appear here soon.</p>
      </main>
    </div>
  );
}

export default App;
"""

    # index.js: Entry point for the React app
    index_js_content = """import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
"""

    # App.css: Styles for the app with a minimalist dark mode (Apple-inspired)
    app_css_content = """body {
  margin: 0;
  padding: 0;
  background-color: #1c1c1e;
  color: #f2f2f7;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.app-container {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.app-header {
  margin-bottom: 2rem;
}

.app-main {
  max-width: 600px;
}
"""

    # Write the files into the frontend folder:
    write_file(os.path.join(frontend_dir, "App.js"), app_js_content)
    write_file(os.path.join(frontend_dir, "index.js"), index_js_content)
    write_file(os.path.join(frontend_dir, "App.css"), app_css_content)

    print("Frontend setup complete. ALL GOOD.")

if __name__ == "__main__":
    main()
