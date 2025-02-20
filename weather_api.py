import os
import requests
import urllib.parse
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# APIキーの取得
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if API_KEY is None:
    raise ValueError("環境変数 'OPENWEATHER_API_KEY' が設定されていません。")

CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# 明示的にエクスポートする関数を定義
__all__ = ["get_weather", "get_forecast"]

def get_weather(city_name):
    """ 指定した都市の現在の天気を取得 """
    params = {
        "q": urllib.parse.quote(city_name),
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]  # アイコンコード
        }
        return weather_info
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_forecast(city_name):
    """ 指定した都市の週間天気を取得 """
    params = {
        "q": urllib.parse.quote(city_name),
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja",
        "cnt": 40  # 5日分のデータを3時間ごとに取得（8回×5日 = 40）
    }
    response = requests.get(FORECAST_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        forecast_dict = {}

        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]  # "YYYY-MM-DD HH:MM:SS" → "YYYY-MM-DD"
            if date not in forecast_dict:
                forecast_dict[date] = {
                    "temp_min": item["main"]["temp"],
                    "temp_max": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "icon": item["weather"][0]["icon"]
                }
            else:
                # 最低・最高気温を更新
                forecast_dict[date]["temp_min"] = min(forecast_dict[date]["temp_min"], item["main"]["temp"])
                forecast_dict[date]["temp_max"] = max(forecast_dict[date]["temp_max"], item["main"]["temp"])

        return forecast_dict
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None