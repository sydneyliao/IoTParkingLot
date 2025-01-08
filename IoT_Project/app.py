from flask import Flask, request, render_template
from parking_logic import load_database, get_parking_spot_for_car
import json

'''app = Flask(__name__,template_folder='Templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_parking():
    car_id = request.form.get('car_id')  # 獲取表單中的車輛 ID
    database = load_database()          # 載入資料庫
    car_info = next((car for car in database["parkingSpots"] if car["carId"] == car_id), None)

    if not car_info:
        return render_template('index.html', message="無法找到該車輛資訊，請確認輸入是否正確。")

    parking_spot = get_parking_spot_for_car(database, car_id)
    if parking_spot:
        park_id = parking_spot.get('parkId')
        #park_time = parking_spot.get('time')
        return render_template('index.html', 
                               message=f"車輛 ID: {car_id} 停在車位: {park_id}")
    else:
        return render_template('index.html', message="該車輛未停在任何車位。")'''
app = Flask(__name__,template_folder='Templates')
@app.route('/query', methods=['POST'])
def query_parking():
    car_id = request.form.get('car_id')  # 從表單獲取 carId
    try:
        # 讀取 car.json 檔案
        with open('car.json', 'r') as file:
            database = json.load(file)
        
        # 遍歷 parkingSpots 找到對應 carId 的 parkId
        parking_spot = next((spot for spot in database["parkingSpots"] if spot["carId"] == int(car_id)), None)

        if parking_spot:
            park_id = parking_spot["parkId"]
            return render_template('index.html', message=f"車輛 ID: {car_id} 停在車位: {park_id}")
        else:
            return render_template('index.html', message=f"車輛 ID: {car_id} 未找到對應的車位。")
    except Exception as e:
        return render_template('index.html', message=f"發生錯誤: {e}")




if __name__ == '__main__':
    app.run(debug=True)
'''import os
print(f"當前工作目錄: {os.getcwd()}")'''