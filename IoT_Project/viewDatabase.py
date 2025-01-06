import json

# 加載資料庫
def load_database(file_path="car.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("can't find database！")
        return {"cars": [], "parkingSpots": []}

# 查看資料庫
def view_database(file_path="car.json"):
    database = load_database(file_path)
    print("plate database：")
    for car in database["cars"]:
        print(f"Car ID: {car['carId']}, UID: {car['uId']}")
    print("\n parking spot：")
    for spot in database["parkingSpots"]:
        print(f"park ID: {spot['parkId']}, distance: {spot['distance']}, status: {spot['status']}")


def menu():
    while True:
        print("1. check")
        print("2. quit")
        choice = input("number: ")
        if choice == "1":
            view_database()
        elif choice == "2":
            print("退出管理工具")
            break
        else:
            print("error")

if __name__ == "__main__":
    menu()
    
