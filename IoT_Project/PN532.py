from adafruit_pn532.i2c import PN532_I2C
import threading
import time

class PN532Handler:
    _lock = threading.Lock()  # 全局鎖，用於 I2C 操作同步

    def __init__(self, tca_mux, channel):
        """
        初始化 PN532Handler 並設置對應的 TCA9548A 通道。
        :param tca_mux: TCA9548A 的多路復用器實例
        :param channel: TCA9548A 的通道 (0~7)
        """
        self.i2c_channel = tca_mux[channel]
        time.sleep(0.1)
        self.pn532 = PN532_I2C(self.i2c_channel)
        self.pn532.SAM_configuration()  # 初始化 PN532

    def detect_card(self, timeout=5.0):
        """
        偵測卡片並返回卡片 ID。
        :param timeout: 偵測卡片的超時時間 (秒)
        :return: 偵測到的卡片 ID 或 None
        """
        with PN532Handler._lock:  # 確保 I2C 操作是同步的
            print("請將卡片放到 PN532 模組上...")
            uid = self.pn532.read_passive_target(timeout=timeout)
            if uid:
                card_id = ''.join([hex(i)[2:] for i in uid])
                print(f"偵測到卡片 ID: {card_id}")
                return card_id
            else:
                print("未偵測到卡片")
                return None    
        

