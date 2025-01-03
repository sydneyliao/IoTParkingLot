import RPi.GPIO as GPIO
import time
import threading

# 假設的 GPIO 引腳分配
LED_GREEN = [24,22,23,27]  # 四個車位的綠燈

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
for pin in LED_GREEN:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # 所有 LED 初始熄滅

# 控制每個車位的綠燈
def control_led(parking_id, parking_status):
    """
    根據車位的狀態控制 LED 燈。
    :param parking_id: 車位編號（從 0 開始）
    :param parking_status: 車位的共享狀態變數
    """
    green_pin = LED_GREEN[parking_id-1]

    while True:
        status = parking_status[parking_id-1]  # 獲取當前車位的狀態

        if status == 0:  # 無車輛，綠燈恆亮
            GPIO.output(green_pin, GPIO.HIGH)

        elif status == 1:  # 指派中，綠燈閃爍
            GPIO.output(green_pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(green_pin, GPIO.LOW)
            time.sleep(0.5)

        elif status == 2:  # 車輛停車，綠燈熄滅
            GPIO.output(green_pin, GPIO.LOW)

        time.sleep(0.1)  # 避免高 CPU 使用率

# 清理 GPIO
def cleanup():
    GPIO.cleanup()
