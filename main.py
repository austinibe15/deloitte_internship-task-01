import json  
import os  
from datetime import datetime  
import unittest  

def load_data(file_name):  
    file_path = os.path.join('C:\\Users\\USER\\Desktop\\TaskDeloitte', file_name)  
    try:  
        with open(file_path, 'r', encoding='utf-8') as file:  
            return json.load(file)  
    except FileNotFoundError:  
        print(f"Error: {file_name} not found in {file_path}")  
        raise  
    except UnicodeDecodeError as e:  
        print(f"Error decoding {file_name}: {e}")  
        raise  

def convert_iso_to_milliseconds(iso_timestamp):  
    dt = datetime.fromisoformat(iso_timestamp[:-1])  
    return int(dt.timestamp() * 1000)  

def unify_data(data1, data2):  
    timestamp_milliseconds = convert_iso_to_milliseconds(data2['timestamp'])  
    unified_data = {  
        "device": {  
            "id": data1["deviceID"],  
            "type": data1["deviceType"]  
        },  
        "timestamp": timestamp_milliseconds,  
        "location": {  
            "country": data2["country"],  
            "city": data2["city"],  
            "area": data2["area"],  
            "factory": data2["factory"],  
            "section": data2["section"]  
        },  
        "data": {  
            "status": data2["data"]["status"],  
            "temperature": data1["temp"]  
        }  
    }  
    return unified_data  

def main():  
    print("Current Working Directory:", os.getcwd())  
    try:  
        data1 = load_data('data-1.json')  
        data2 = load_data('data-2.json')  
        result = unify_data(data1, data2)  
        
        with open('data-result.json', 'w', encoding='utf-8') as outfile:  
            json.dump(result, outfile, indent=4)  
        
    except Exception as e:  
        print(f"An error occurred: {e}")  

#### Unit Testing ####  

class TestDataProcessing(unittest.TestCase):  
    
    def setUp(self):  
        self.data1 = load_data('data-1.json')  
        self.data2 = load_data('data-2.json')  
        
    def test_unify_data(self):  
        expected_data = {  
            "device": {  
                "id": self.data1["deviceID"],  
                "type": self.data1["deviceType"]  
            },  
            "timestamp": convert_iso_to_milliseconds(self.data2['timestamp']),  
            "location": {  
                "country": self.data2["country"],  
                "city": self.data2["city"],  
                "area": self.data2["area"],  
                "factory": self.data2["factory"],  
                "section": self.data2["section"]  
            },  
            "data": {  
                "status": self.data2["data"]["status"],  
                "temperature": self.data1["temp"]  
            }  
        }  
        result = unify_data(self.data1, self.data2)  
        self.assertEqual(result, expected_data)  

if __name__ == "__main__":  
    main()  
    unittest.main()