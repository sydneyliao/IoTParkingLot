'''from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# 初始化伺服馬達 (將 GPIO 17 設定為輸出)
factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)


# 讓伺服馬達旋轉到順時針 90 度的位置
print("fence up")
servo.value = -1  # 完全時針旋轉
sleep(3)

# 將伺服馬達返回中心
print("fence down")
servo.value = 0  # 中心位置
sleep(1)

# 如果需要停止控制，釋放伺服馬達
print("release")
servo.detach()'''

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

class ServoController:
    def __init__(self, gpio_pin=17):
        factory = PiGPIOFactory()
        self.servo = Servo(gpio_pin, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)

    def fence_up(self, duration=3):
        """升起柵欄"""
        print("柵欄升起")
        self.servo.value = -1  # 完全順時針旋轉
        sleep(duration)

    def fence_down(self, duration=1):
        """降下柵欄"""
        print("柵欄降下")
        self.servo.value = 0  # 中心位置
        sleep(duration)

    def release(self):
        """釋放伺服馬達"""
        print("釋放伺服馬達")
        self.servo.detach()
