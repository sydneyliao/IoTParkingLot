# IoT Smart Parking System

## Introduction
The system will navigate entering vehicles to the parking space closest to the store entrance. The LED light blinks so the drivers can see the parking space in a short time and save time walking to the entrance.

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
![Circuit Diagram 1](C:\Users\User\OneDrive\圖片\螢幕擷取畫面\1735885506652.jpg)
![Circuit Diagram 2](C:\Users\User\OneDrive\圖片\螢幕擷取畫面\1735885530442.jpg)

Since the Python version on the Raspberry Pi is 3.7 but this project requires Python 3.8, to simplify operations, please first download Python 3.8 and then create a virtual environment to run the program within it. The instructions are as follows:

---

### Steps

#### 1. Install Python 3.8
[Instructions for installation](https://itheo.tech/install-python-38-on-a-raspberry-pi).

Check version by entering:
```bash
python3.8 --version




