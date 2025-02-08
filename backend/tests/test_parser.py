import unittest
from parsers.sleep_parser import parse_sleep_data

class TestSleepParser(unittest.TestCase):
    def test_parse_sleep_data(self):
        sample_xml = '''
        <HealthData>
            <Record type="HKCategoryTypeIdentifierSleepAnalysis" startDate="2025-02-01T23:00:00" endDate="2025-02-02T07:00:00" value="Asleep"/>
        </HealthData>
        '''
        with open("test_export.xml", "w") as f:
            f.write(sample_xml)
        
        result = parse_sleep_data("test_export.xml")
        self.assertEqual(len(result["durations"]), 1)
        self.assertEqual(result["durations"][0], 8.0)

if __name__ == "__main__":
    unittest.main()
