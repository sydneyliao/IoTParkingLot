import json
def load_database(file_path="car.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("資料庫文件未找到！")
        return {"cars": [], "parkingSpots": []}

def save_database(database, file_path="car.json"):
    with open(file_path, "w") as file:
        json.dump(database, file, indent=4)
