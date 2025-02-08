//
//  HealthDataManager.swift
//  SleepTracker
//
//  Created by [Your Name] on [Date].
//

import Foundation
import HealthKit

class HealthDataManager {
    // HealthKit store instance.
    let healthStore = HKHealthStore()
    
    /// Requests authorization to access HealthKit sleep analysis data.
    /// - Parameter completion: A closure that receives a success flag and an optional error.
    func requestAuthorization(completion: @escaping (Bool, Error?) -> Void) {
        // Define the sleep analysis type.
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            let error = NSError(domain: "HealthKit", code: 1, userInfo: [NSLocalizedDescriptionKey: "Sleep data type not available"])
            completion(false, error)
            return
        }
        
        // Request read access for the sleep analysis type.
        let typesToRead: Set<HKObjectType> = [sleepType]
        healthStore.requestAuthorization(toShare: nil, read: typesToRead) { (success, error) in
            DispatchQueue.main.async {
                completion(success, error)
            }
        }
    }
    
    /// Fetches the most recent sleep analysis data.
    /// - Parameter completion: A closure that returns an array of HKCategorySample objects or an error.
    func fetchSleepData(completion: @escaping ([HKCategorySample]?, Error?) -> Void) {
        #if targetEnvironment(simulator)
        // Running in the simulator: simulate a response.
        print("Running in simulator: returning dummy sleep data.")
        // Since HKCategorySample objects are read-only and difficult to simulate,
        // we return an empty array here. You can modify this to return custom dummy data if needed.
        completion([], nil)
        #else
        // Running on a real device: fetch sleep data from HealthKit.
        guard let sleepType = HKObjectType.categoryType(forIdentifier: .sleepAnalysis) else {
            let error = NSError(domain: "HealthKit", code: 1, userInfo: [NSLocalizedDescriptionKey: "Sleep data type not available"])
            completion(nil, error)
            return
        }
        
        // Sort descriptor to get the most recent sleep samples first.
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        
        // Create a query to fetch up to 10 recent sleep samples.
        let query = HKSampleQuery(sampleType: sleepType, predicate: nil, limit: 10, sortDescriptors: [sortDescriptor]) { (query, samples, error) in
            if let error = error {
                DispatchQueue.main.async {
                    completion(nil, error)
                }
                return
            }
            
            if let sleepSamples = samples as? [HKCategorySample] {
                DispatchQueue.main.async {
                    completion(sleepSamples, nil)
                }
            } else {
                let castError = NSError(domain: "HealthKit", code: 2, userInfo: [NSLocalizedDescriptionKey: "Failed to cast samples to HKCategorySample"])
                DispatchQueue.main.async {
                    completion(nil, castError)
                }
            }
        }
        
        // Execute the HealthKit query.
        healthStore.execute(query)
        #endif
    }
}
