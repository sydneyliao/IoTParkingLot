# IoT Smart Parking System
NCU MIS IoT Project By Hsin Ni Liao
## Introduction
The system will navigate entering vehicles to the parking space closest to the store entrance. The LED light blinks so the drivers can see the parking space in a short time and save time walking to the entrance.
<img src="" alt="final" title="final" width="300">
<img src="images/IoT_circuit.png" alt="circuit" title="circuit" width="500">


## Hardwares
- **RaspberryPi 4**
- **Breadboard**
- **Lots of dupont lines** (male/male, male/female, male/male)
- **TCA9548A**
- **PN532** x5 (may modify to fit your needs)*
- **RFID sticker** (13.56M 26MM ISO 14443A)
- **SG90 servo motor**
- **Green LED** x4 (depends on how many parking spots)*
- **Popsicle sticks**
- **Foamboard**
- **Circuit Diagram**

## Setup
Since the PN532 uses I2C communication, make sure I2C is enabled.

<img src="images/1735885506652.jpg" alt="raspberryPi setup" title="raspberryPi setup" width="300">
<img src="images/1735885530442.jpg" alt="interface" title="interface" width="300">

Since the Python version on the Raspberry Pi is 3.7 but this project requires Python 3.8, to simplify operations, please first download Python 3.8 and then create a virtual environment to run the program within it. The instructions are as follows:

---

### Steps

#### 1. Install Python 3.8
[Instructions for installation](https://itheo.tech/install-python-38-on-a-raspberry-pi).

Check version by entering:

``python3.8 --version``

<img src="images/螢幕擷取畫面 2025-01-03 152728.png" alt="raspberryPi setup" title="raspberryPi setup" width="300">

Success!
#### 2.	Update the System and Install Required Tools
Make sure your Raspberry Pi system is up to date and install the necessary tools for creating virtual environments.

``
sudo apt update
sudo apt upgrade -y
sudo apt install python3-venv -y``

#### 3.	Create the Virtual Environment
Navigate to your desired directory and create a virtual environment named my_env:

``python3 -m venv my_env``

Replace my_env with your preferred name for the virtual environment.This command creates a folder named my_env in the current directory, which contains all the necessary files for the virtual environment.
#### 4.	Activate the Virtual Environment
To start using the virtual environment, activate it with the following command:

``source my_env/bin/activate``

Once activated, your terminal prompt will show (my_env), indicating that you are now working inside the virtual environment.
 
<img src="images/螢幕擷取畫面 2025-01-03 144459.png" alt="raspberryPi setup" title="raspberryPi setup" width="300">

#### 5.	Deactivate the Virtual Environment
When you're done working in the virtual environment, deactivate it using:
``deactivate``

This will return you to the global Python environment.
### Install packages
#### For PN532:
``pip install adafruit-circuitpython-pn532``

if there’s an error message, enter 

``pip install adafruit-blinka adafruit-circuitpython-busdevice``

#### For servo motor

``pip install gpiozero``

``pip install pigpio``(make sure to enter sudo pigpiod before running the code)
#### For TCA9548A
``pip install adafruit-circuitpython-tca9548a``

if there’s an error message, enter

``pip install adafruit-blinka adafruit-circuitpython-busdevice``
### Program Code
All codes are in the folder “IoT_Project”, you may download them and have a closer look. Some further details will be explained below:

#### 1. PN532.py
To check if the I2C devices are connected, enter i2cdetect -y 1. If the output matches the example shown in the image below, your TCA9548A has been successfully connected.

To verify each PN532 on its respective channel, you can use the code below. It's recommended to check each channel individually, as this makes it easier to identify any issues that may arise.
```
import board
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

def verify_tca9548a_channel(tca, channel):
    print(f"切換到通道 {channel}...")
    try:
        i2c_channel = tca[channel]
        if i2c_channel.try_lock():
            print(f"成功鎖定通道 {channel}")
            i2c_channel.unlock()
        else:
            print(f"無法鎖定通道 {channel}")
    except Exception as e:
        print(f"通道 {channel} 錯誤: {e}")

# 主程式
if __name__ == "__main__":
    print("開始測試 TCA9548A I2C 多路復用器")
    scan_i2c_devices(tca)  # 掃描所有通道上的 I2C 設備
    verify_tca9548a_channel(tca, 0)
    test_single_channel(tca, 0)
    # 測試 PN532 功能（視通道決定）
    for channel in [0,1,3,4]:
        test_pn532_on_channel(tca, channel)
```
You should see something like this:


#### 2.	Motor.py
Depends on the angle you want your fence to go up and down, you may change the code. For more detail,visit [Control motor](https://docs.sunfounder.com/projects/umsk/en/latest/05_raspberry_pi/pi_lesson33_servo.html).
#### 3. clear.py and viewDatabase.py
These two files allow programmer to 



        



