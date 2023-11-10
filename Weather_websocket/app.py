import asyncio
import websockets
import requests
import json

async def weather_data(websocket, path):
    try:
        while True:
            city = await websocket.recv()

            api_key = "30d4741c779ba94c470ca1f63045390a"
            weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"
            response = requests.get(weather_api_url)
            weather_data = response.json()

            weather_data['main']['temp'] = convert_to_celsius(weather_data['main']['temp'])

            # Send weather data to the connected client
            await websocket.send(json.dumps(weather_data))

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed for {path}")

def convert_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9)

start_server = websockets.serve(weather_data, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
