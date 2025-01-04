import json

def reset_parking_spots(file_path="car.json"):
    try:
        # 加載資料庫
        with open(file_path, "r") as file:
            database = json.load(file)

        # 遍歷停車位數據
        for spot in database.get("parkingSpots", []):
            if spot["status"] == 1 or spot["status"] == 2:  # 如果狀態為1或2，重置為0
                spot["status"] = 0
                spot["carId"] = None

        # 保存更新後的資料庫
        with open(file_path, "w") as file:
            json.dump(database, file, indent=4)

        print("成功重置！")

    except FileNotFoundError:
        print("文件未找到！")
    except json.JSONDecodeError:
        print("文件格式error！")
    except Exception as e:
        print(f"error:{e}")

# 調用函数
reset_parking_spots()
