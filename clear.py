import json

def reset_parking_spots(file_path="car.json"):
    """
    重置所有状态为 1 的停车位状态为 0。
    :param file_path: 数据库文件路径
    """
    try:
        # 加载数据库
        with open(file_path, "r") as file:
            database = json.load(file)

        # 遍历停车位数据，重置状态
        for spot in database.get("parkingSpots", []):
            if spot["status"] == 1 or spot["status"] == 2:  # 如果状态为 1，则重置为 0
                spot["status"] = 0
                spot["carId"] = None

        # 保存更新后的数据库
        with open(file_path, "w") as file:
            json.dump(database, file, indent=4)

        print("成功重置！")

    except FileNotFoundError:
        print("文件未找到！")
    except json.JSONDecodeError:
        print("文件格式error！")
    except Exception as e:
        print(f"error:{e}")

# 调用函数
reset_parking_spots()