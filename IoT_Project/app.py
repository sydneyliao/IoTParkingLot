from flask import Flask, request, render_template
from parking_logic import load_database, get_parking_spot_for_car
import json
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
