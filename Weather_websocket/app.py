import asyncio
import websockets
import requests
import json

async def weather_data(websocket, path):
    try:
        while True:
            # Nhận tên thành phố từ Client
            city = await websocket.recv()

            # Lấy dữ liệu thời tiết cho thành phố đã chọn
            api_key = "30d4741c779ba94c470ca1f63045390a"
            weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
            response = requests.get(weather_api_url)
            weather_data = response.json()

            # Chuyển đổi nhiệt độ sang đơn vị Celsius
            weather_data['main']['temp'] = convert_to_celsius(weather_data['main']['temp'])

            # Gửi dữ liệu thời tiết về cho client kết nối
            await websocket.send(json.dumps(weather_data))

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed for {path}")

# Hàm chuyển đổi đơn vị nhiệt độ từ Fahrenheit sang Celsius:
def convert_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9)

# Tạo một server WebSocket lắng nghe trên địa chỉ "localhost" và cổng 8765.
start_server = websockets.serve(weather_data, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
