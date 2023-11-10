from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Điều hướng trang chủ
def weather(city):
    api_key = '30d4741c779ba94c470ca1f63045390a'
    
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")

    if weather_data.status_code == 200:
        data = weather_data.json()
        weather = data['weather'][0]['main']
        temp_fahrenheit = data['main']['temp']
        temp_celsius = round((temp_fahrenheit - 32) * 5/9)  
        return f"Thành phố: { city } Nhiệt độ: { temp_celsius }ºC Thời tiết: { weather }"
    else:
        return "Thành phố không tồn tại, vui lòng thử lại."


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        reponse = weather(city)
        return render_template("weather.html", weather=reponse)
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)
