import os

def write_file(filepath, content):
    """Write content to a file at the given filepath."""
    with open(filepath, "w") as f:
        f.write(content)

def main():
    # Assume current working directory is the project root: apple-sleep-insights
    current_dir = os.getcwd()
    ios_app_dir = os.path.join(current_dir, "ios-app")
    os.makedirs(ios_app_dir, exist_ok=True)
    
    # Content for HealthDataManager.swift
    health_data_manager_content = """\
import HealthKit

class HealthDataManager {
    let healthStore = HKHealthStore()
    
    // Request authorization to read sleep data
    func requestAuthorization(completion: @escaping (Bool, Error?) -> Void) {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            completion(false, NSError(domain: "HealthKit", code: 1, userInfo: [NSLocalizedDescriptionKey: "Sleep data type not available"]))
            return
        }
        let typesToRead: Set = [sleepType]
        healthStore.requestAuthorization(toShare: nil, read: typesToRead) { success, error in
            completion(success, error)
        }
    }
    
    // Fetch the most recent sleep samples (dummy implementation for now)
    func fetchSleepData(completion: @escaping ([HKCategorySample]?, Error?) -> Void) {
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            completion(nil, NSError(domain: "HealthKit", code: 1, userInfo: [NSLocalizedDescriptionKey: "Sleep data type not available"]))
            return
        }
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        let query = HKSampleQuery(sampleType: sleepType, predicate: nil, limit: 10, sortDescriptors: [sortDescriptor]) { (_, samples, error) in
            guard let samples = samples as? [HKCategorySample] else {
                completion(nil, error)
                return
            }
            completion(samples, nil)
        }
        healthStore.execute(query)
    }
}
"""
    # Content for SleepTrackerApp.swift
    sleep_tracker_app_content = """\
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
                        sleepData = "Authorization failed: \\(error?.localizedDescription ?? "Unknown error")"
                    }
                }
            }
        }
    }
    
    func fetchAndSendSleepData() {
        healthDataManager.fetchSleepData { samples, error in
            if let error = error {
                DispatchQueue.main.async {
                    sleepData = "Error fetching data: \\(error.localizedDescription)"
                }
                return
            }
            if let samples = samples {
                let dataSummary = "Fetched \\(samples.count) sleep samples."
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
            print("Error creating JSON: \\(error)")
            return
        }
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending data: \\(error)")
                return
            }
            guard let data = data else {
                print("No data received from backend")
                return
            }
            if let responseString = String(data: data, encoding: .utf8) {
                print("Response from backend: \\(responseString)")
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
"""

    write_file(os.path.join(ios_app_dir, "HealthDataManager.swift"), health_data_manager_content)
    write_file(os.path.join(ios_app_dir, "SleepTrackerApp.swift"), sleep_tracker_app_content)
    
    print("iOS app setup complete. ALL GOOD.")

if __name__ == "__main__":
    main()
