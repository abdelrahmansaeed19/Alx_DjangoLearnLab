import json

def process_json(data: dict, file_path: str) -> dict:
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    with open(file_path, 'r') as file:
        return json.load(file)
    
data = {'name': 'Alice', 'age': 30, 'city': 'Kampala'}

print(process_json(data, 'data.json'))