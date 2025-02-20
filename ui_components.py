from PySide6.QtWidgets import QComboBox, QLabel
from PySide6.QtGui import QPixmap
import requests
from io import BytesIO

def create_prefecture_selector():
    """ 都道府県選択用のコンボボックスを作成 """
    prefecture_selector = QComboBox()
    prefectures = ["東京都", "大阪府", "北海道", "愛知県", "福岡県", "神奈川県", "埼玉県", "千葉県"]
    prefecture_selector.addItems(prefectures)
    return prefecture_selector

def create_city_selector():
    """ 市町村選択用のコンボボックスを作成 """
    city_selector = QComboBox()
    return city_selector

def create_weather_icon():
    """ 天気アイコン表示用の QLabel を作成 """
    label_icon = QLabel()
    label_icon.setFixedSize(100, 100)
    return label_icon

def update_weather_icon(label, icon_code):
    """ 天気アイコンを更新 """
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url)
    
    if response.status_code == 200:
        pixmap = QPixmap()
        pixmap.loadFromData(BytesIO(response.content).read())
        label.setPixmap(pixmap)
    else:
        label.clear()