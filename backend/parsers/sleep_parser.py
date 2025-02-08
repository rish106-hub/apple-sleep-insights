import xml.etree.ElementTree as ET
from datetime import datetime

def parse_sleep_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sleep_data = []

    for record in root.findall("Record"):
        if record.get("type") == "HKCategoryTypeIdentifierSleepAnalysis":
            sleep_data.append({
                "start": record.get("startDate"),
                "end": record.get("endDate"),
                "value": record.get("value"),
            })

    durations = [
        {
            "date": entry["start"].split("T")[0],
            "duration": calculate_duration(entry["start"], entry["end"]),
        }
        for entry in sleep_data
    ]
    
    return {
        "summary": f"Processed {len(durations)} sleep records.",
        "durations": [entry["duration"] for entry in durations],
        "dates": [entry["date"] for entry in durations],
    }

def calculate_duration(start, end):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    return round((end_dt - start_dt).total_seconds() / 3600, 2)
