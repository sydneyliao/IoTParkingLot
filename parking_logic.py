import json


def load_database(file_path="car.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("文件未找到！")
        return {"cars": [], "parkingSpots": []}

# 保存数据库
def save_database(database, file_path="car.json"):
    with open(file_path, "w") as file:
        json.dump(database, file, indent=4)

# find plate
def find_car_by_uid(uid, cars):
    for car in cars:
        if car["uId"] == uid:
            return car["carId"]
    return None

# 分配最近的可用parking spot
def assign_parking_spot(database, car_id, parking_status):
    parking_spots = database["parkingSpots"]
    available_spots = [spot for spot in parking_spots if spot["status"] == 0]
    if not available_spots:
        print("parking spot full!")
        return None
    closest_spot = min(available_spots, key=lambda spot: spot["distance"])
    closest_spot["status"] = 1  
    closest_spot["carId"] = car_id
    print(f"Car {car_id} please go to  {closest_spot['parkId']} (distance: {closest_spot['distance']})")
    parking_status[closest_spot["parkId"] - 1] = 1 
    return closest_spot

def get_parking_spot_for_car(database, car_id):
    for spot in database["parkingSpots"]:
        if spot["carId"] == car_id and spot["status"]==1:
            return spot
    return None