🛌 Apple Sleep Insights

Track, Analyze & Improve Your Sleep with AI-Driven Insights
A modern web-based tool that processes Apple Health sleep data to provide deep insights & recommendations based on your sleep patterns.


📌 Features

✅ Upload Apple Health .zip files (exported from iOS)
✅ AI-powered sleep analysis (Duration, Deep Sleep, Quality Score)
✅ Beautiful, Apple-inspired UI (Smooth, Responsive, Dark Mode)
✅ Interactive Charts & Graphs (Sleep Trends, Weekly Analysis)
✅ Backend with Flask API (Processes Apple Health data)
✅ Front-end with React & Parcel (Fast, Lightweight, Beautiful)

📁 Project Structure

apple-sleep-insights/
│
├── backend/                     # Backend logic (Flask API)
│   ├── app.py                   # Main backend server
│   ├── requirements.txt          # Backend dependencies
│   ├── uploads/                  # Folder for uploaded `.zip` files
│   ├── parsers/                  # XML parsing logic for Apple Health data
│   │   └── sleep_parser.py       # Sleep data extraction logic
│   ├── tests/                    # Unit tests for backend
│   │   └── test_parser.py        # Testing sleep data parsing
│   └── README.md                 # Backend documentation
│
├── frontend/                     # Frontend logic (React + Parcel)
│   ├── public/                   # Static assets
│   │   └── index.html            # Main HTML file
│   ├── src/                      # React source files
│   │   ├── components/           # Reusable React components
│   │   │   ├── UploadForm.jsx    # Upload form component
│   │   │   ├── InsightsDashboard.jsx  # Dashboard for insights
│   │   ├── App.jsx               # Main React App entry point
│   │   ├── index.js              # React DOM entry point
│   │   └── styles.css            # Global CSS styling
│   ├── package.json              # Frontend dependencies
│   └── README.md                 # Frontend documentation
│
├── automate/                     # Automation scripts
│   ├── foldercreation.py         # Creates the folder structure
│   ├── automate_backend.py       # Automates backend setup
│   ├── automate_frontend.py      # Automates frontend setup
│   ├── automate_integration.py   # Integrates frontend & backend
│   ├── automate_all.py           # Runs all automation scripts
│   ├── iphonefix.py              # Fixes iOS-related issues
│   └── abc.py                    # Fixes frontend UI issues
│
├── ios-app/                      # Placeholder for iOS integration
│   ├── SleepTracker/             # iOS project files
│   ├── SleepTrackerTests/        # Unit tests for iOS
│   ├── SleepTrackerUITests/      # UI tests for iOS
│   └── README.md                 # iOS documentation
│
├── README.md                     # This file (Main project README)
└── .gitignore                     # Ignore unnecessary files

🚀 Getting Started

Follow these steps to set up and run the project.

1️⃣ Backend Setup
Install Dependencies

cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt

Start the Backend Server
python3 app.py
The backend will start at http://localhost:5000/.

2️⃣ Frontend Setup
Install Dependencies

cd frontend
npm install
Start the Frontend

npm start
The frontend will be available at http://localhost:1234/.

3️⃣ Upload Sleep Data
Export your Apple Health Data as a .zip file.
Visit the frontend at http://localhost:1234/.
Click Upload and select your .zip file.
The backend processes the file and displays insights.
🧑‍💻 API Endpoints

Method	Endpoint	Description
GET	/	Check if the backend is running
POST	/upload	Upload Apple Health .zip file and get insights
📊 Example API Response

{
  "summary": "Processed 7 sleep records.",
  "sleep_score": 85,
  "insights": [
    {
      "date": "2025-02-01",
      "duration": 7.5
    },
    {
      "date": "2025-02-02",
      "duration": 8.2
    }
  ]
}

🛠️ Troubleshooting

Backend Issues
Issue: ModuleNotFoundError: No module named 'flask'
Fix: Run pip install flask inside the backend directory.
Issue: OSError: Address already in use
Fix: Find and kill the process using port 5000:
lsof -i :5000
kill -9 <PID>
Frontend Issues
Issue: npm start not working
Fix: Ensure "scripts" in package.json contains:
"scripts": {
  "start": "parcel index.html"
}
Then, restart with:

npm start
Issue: Failed to resolve 'styles.css'
Fix: Ensure styles.css exists in the frontend folder.
🤝 Contributing

Contributions are welcome!
To contribute:

Fork the repository
Create a new branch
Make your changes
Submit a pull request (PR)
📝 License

This project is open-source and available under the MIT License.

