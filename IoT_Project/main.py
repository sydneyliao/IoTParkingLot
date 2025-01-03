import threading
import board
import busio
from adafruit_tca9548a import TCA9548A
from PN532 import PN532Handler
from motor import ServoController
import signal
import sys
import time
from database import load_database
from parking_logic import save_database
from parking_logic import load_database, save_database, find_car_by_uid, assign_parking_spot,get_parking_spot_for_car
from led_control import control_led, cleanup
scanned_cars = set()
scanned_cars_lock = threading.Lock()

# 處理 Ctrl+C 信號以安全退出
def signal_handler(sig, frame):
    print("\n偵測到中斷信號 (Ctrl+C)，結束程式...")
    sys.exit(0)

def handle_channel_1(tca, servo_controller,parking_status):
    """處理通道 1 的 PN532 功能：控制柵欄並分配車位"""
    pn532_handler_ch1 = PN532Handler(tca, channel=1)
    database = load_database()  
    while True:
        card_id = pn532_handler_ch1.detect_card(timeout=5.0)
        if card_id:
            print(f"通道 1 偵測到卡片 ID: {card_id}")
            car_id = find_car_by_uid(card_id, database["cars"])
            if not car_id:
                print("無法分配車位，未知車輛！")
                continue
            print(f"找到車輛: Car {car_id}")
            assigned_spot = assign_parking_spot(database, car_id,parking_status)
            if assigned_spot:
                save_database(database)  
                servo_controller.fence_up(duration=3)  # 柵欄升起
                servo_controller.fence_down(duration=1)  # 柵欄降下

                # 記錄車輛到共享的集合中
                with scanned_cars_lock:
                    scanned_cars.add(car_id)
                    print(f"已記住車輛: {scanned_cars}")

parking_status = [0, 0, 0, 0]
def handle_parking_spot(tca, channel, park_id):
    """
    處理車位的 PN532 功能：根據掃描結果更新車位狀態和資料庫。
    :param tca: TCA9548A 多路復用器實例
    :param channel: PN532 的通道編號
    :param park_id: 車位的 parkId
    """
    pn532_handler = PN532Handler(tca, channel=channel)
    while True:
        card_id = pn532_handler.detect_card(timeout=5.0)
        database = load_database()  # 每次更新資料庫
        parking_spot = next((spot for spot in database["parkingSpots"] if spot["parkId"] == park_id), None)
        if not parking_spot:
            print(f"車位 {park_id} 未找到！")
            continue

        if card_id:
            car_id = find_car_by_uid(card_id, database["cars"])
            with scanned_cars_lock:  
                if not car_id in scanned_cars:
                    print(f"通道 {channel}: 無法辨識車輛")
                    continue
            if car_id:
                # 更新車位狀態為已停車
                parking_spot["status"] = 2
                parking_spot["carId"] = car_id
                print(f"車位 {park_id} 偵測到車輛 {car_id}，綠燈熄滅")
                parking_status[park_id - 1] = 2  # 更新共享狀態
            else:
                print(f"車位 {park_id} 偵測到未知車輛，狀態保持不變")
        else:
            # 無車輛，恢復為指派狀態（閃爍）或未分配狀態（恆亮）
            if parking_spot["status"] == 2:
                parking_spot["status"] = 0  # 恢復為指派狀態
                parking_spot["carId"] = None
                print(f"車位 {park_id} 無車輛，綠燈恆亮")
                parking_status[park_id - 1] = 0 # 更新共享狀態

        save_database(database)  # 保存更新後的資料庫
        
def main():
    signal.signal(signal.SIGINT, signal_handler)
    i2c = busio.I2C(board.SCL, board.SDA)
    tca = TCA9548A(i2c)

    # 初始化伺服馬達
    servo_controller = ServoController()
    print("系統啟動，按下 Ctrl+C 停止程式...")
    threads=[]
    thread_ch1 = threading.Thread(target=handle_channel_1, args=(tca, servo_controller, parking_status), daemon=True)
    thread_ch1.start()
    parking_channels=[(0,1),(3,2),(4,3),(5,4)]  # 方向指示的通道列表
    for channel,park_id in parking_channels:
        thread = threading.Thread(target=handle_parking_spot, args=(tca, channel,park_id), daemon=True)
        threads.append(thread)
        thread.start()
    for i in range(1,5):  # 假設有 4 個車位
        thread = threading.Thread(target=control_led, args=(i, parking_status), daemon=True)
        thread.start()
        threads.append(thread)    
    # 主執行緒保持運行
    try:
        while True:
            pass  # 主程式保持運行
    except KeyboardInterrupt:
        print("程式結束")
        servo_controller.release()
        save_database(load_database())
        sys.exit(0)

if __name__ == "__main__":
    main()

