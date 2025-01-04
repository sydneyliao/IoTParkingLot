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




