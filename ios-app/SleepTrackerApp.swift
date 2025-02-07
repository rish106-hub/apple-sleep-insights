import SwiftUI
import HealthKit

struct SleepTrackerApp: View {
    @State private var sleepData: String = "No data"
    let healthDataManager = HealthDataManager()
    
    var body: some View {
        VStack {
            Text("Sleep Tracker")
                .font(.largeTitle)
                .padding()
            Text(sleepData)
                .padding()
            Button("Fetch Sleep Data") {
                fetchAndSendSleepData()
            }
            .padding()
        }
        .onAppear {
            healthDataManager.requestAuthorization { success, error in
                if !success {
                    DispatchQueue.main.async {
                        sleepData = "Authorization failed: \(error?.localizedDescription ?? "Unknown error")"
                    }
                }
            }
        }
    }
    
    func fetchAndSendSleepData() {
        healthDataManager.fetchSleepData { samples, error in
            if let error = error {
                DispatchQueue.main.async {
                    sleepData = "Error fetching data: \(error.localizedDescription)"
                }
                return
            }
            if let samples = samples {
                let dataSummary = "Fetched \(samples.count) sleep samples."
                DispatchQueue.main.async {
                    sleepData = dataSummary
                }
                // Send data to the Flask backend
                sendDataToBackend(sleepSummary: dataSummary)
            }
        }
    }
    
    func sendDataToBackend(sleepSummary: String) {
        guard let url = URL(string: "http://localhost:5000/upload_sleep_data") else {
            return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let json: [String: Any] = ["sleep": sleepSummary]
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: json, options: [])
        } catch {
            print("Error creating JSON: \(error)")
            return
        }
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending data: \(error)")
                return
            }
            guard let data = data else {
                print("No data received from backend")
                return
            }
            if let responseString = String(data: data, encoding: .utf8) {
                print("Response from backend: \(responseString)")
            }
        }
        task.resume()
    }
}

struct SleepTrackerApp_Previews: PreviewProvider {
    static var previews: some View {
        SleepTrackerApp()
    }
}
