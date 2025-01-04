'''import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_pn532.i2c import PN532_I2C
import time

# 初始化 I2C 和 TCA9548A
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCA9548A(i2c)

# 測試每個通道上的 I2C 設備
def scan_i2c_devices(tca_mux):
    for channel in range(8):  # TCA9548A 有 8 個通道 (CH0 ~ CH7)
        print(f"changing to 通道{channel}...")
        try:
            i2c_channel = tca_mux[channel]  # 選擇 TCA9548A 的通道
            i2c_channel.try_lock()
            devices = i2c_channel.scan()  # 掃描 I2C 設備地址
            i2c_channel.unlock()
            
            if devices:
                print(f"通道 {channel} 上找到的設備地址: {[hex(address) for address in devices]}")
            else:
                print(f"通道 {channel} 上沒有找到設備")
        except Exception as e:
            print(f"通道 {channel} 錯誤: {e}")
            

# 測試 PN532 模組功能
def test_pn532_on_channel(tca_mux, channel):
    print(f"正在測試通道 {channel} 上的 PN532...")
    try:
        i2c_channel = tca_mux[channel]
        time.sleep(0.2)
        pn532 = PN532_I2C(i2c_channel)
        pn532.SAM_configuration()  # 初始化 PN532

        print("請將卡片放到 PN532 模組上...")
        uid = pn532.read_passive_target(timeout=2.0)
        if uid:
            card_id = ''.join([hex(i)[2:] for i in uid])
            print(f"通道 {channel} 偵測到卡片 ID: {card_id}")
        else:
            print(f"通道 {channel} 未偵測到卡片")
    except Exception as e:
        print(f"通道 {channel} 錯誤: {e}")

def test_pn532_on_channel(tca_mux, channel):
    print(f"正在測試通道 {channel} 上的 PN532...")
    try:
        i2c_channel = tca_mux[channel]
        pn532 = PN532_I2C(i2c_channel)
        pn532.SAM_configuration()  # 初始化 PN532

        print("請將卡片放到 PN532 模組上...")
        uid = pn532.read_passive_target(timeout=5.0)
        if uid:
            card_id = ''.join([hex(i)[2:] for i in uid])
            print(f"通道 {channel} 偵測到卡片 ID: {card_id}")
        else:
            print(f"通道 {channel} 未偵測到卡片")
    except Exception as e:
        print(f"通道 {channel} 錯誤: {e}")
        
        
def test_single_channel(tca, channel):
    print(f"正在測試通道 {channel}...")
    try:
        i2c_channel = tca[channel]
        if i2c_channel.try_lock():
            devices = i2c_channel.scan()
            print(f"通道 {channel} 上的設備地址: {[hex(addr) for addr in devices]}")
            i2c_channel.unlock()
            if 0x24 in devices:
                print(f"通道 {channel} 上檢測到 PN532（地址 0x24）")
            else:
                print(f"通道 {channel} 未檢測到 PN532（地址 0x24）")
        else:
            print(f"無法鎖定通道 {channel}")
    except Exception as e:
        print(f"通道 {channel} 測試失敗: {e}")

# 主程序


def verify_tca9548a_channel(tca, channel):
    print(f"切换到通道 {channel}...")
    try:
        i2c_channel = tca[channel]
        if i2c_channel.try_lock():
            print(f"成功锁定通道 {channel}")
            i2c_channel.unlock()
        else:
            print(f"无法锁定通道 {channel}")
    except Exception as e:
        print(f"通道 {channel} 错误: {e}")

# 主程式
if __name__ == "__main__":
    print("開始測試 TCA9548A I2C 多路復用器")
    scan_i2c_devices(tca)  # 掃描所有通道上的 I2C 設備
    verify_tca9548a_channel(tca, 0)
    test_single_channel(tca, 0)
    # 測試 PN532 功能（假設 PN532 在通道 0 和通道 1）
    for channel in [0,1,3,4]:
        test_pn532_on_channel(tca, channel)'''
        
     

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
        

