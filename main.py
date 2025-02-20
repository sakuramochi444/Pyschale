import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from weather_api import get_weather, get_forecast
from ui_components import create_prefecture_selector, create_city_selector, create_weather_icon, update_weather_icon
from city_mappings import prefecture_city_map, city_name_map

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("天気アプリ")
        self.setGeometry(100, 100, 400, 400)

        # 背景色の設定
        self.setStyleSheet("background-color: white;")

        # レイアウト
        main_layout = QVBoxLayout()

        # タイトルラベル
        title_label = QLabel("天気情報取得アプリ")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 都道府県と市町村の選択レイアウト
        selection_layout = QHBoxLayout()

        # 都道府県選択
        self.prefecture_selector = create_prefecture_selector()
        self.prefecture_selector.currentIndexChanged.connect(self.update_city_selector)
        selection_layout.addWidget(self.prefecture_selector)

        # 市町村選択
        self.city_selector = create_city_selector()
        selection_layout.addWidget(self.city_selector)

        main_layout.addLayout(selection_layout)

        # 天気アイコン
        self.weather_icon = create_weather_icon()
        self.weather_icon.setStyleSheet("background-color: #E6FFE6; border: 1px solid #CCCCCC;")
        main_layout.addWidget(self.weather_icon, alignment=Qt.AlignCenter)

        # 現在の天気
        self.label_weather = QLabel("天気情報を取得してください")
        self.label_weather.setFont(QFont("Arial", 14))
        self.label_weather.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_weather)

        # 週間天気
        self.label_forecast = QLabel("")
        self.label_forecast.setFont(QFont("Arial", 12))
        self.label_forecast.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_forecast)

        # ボタン
        self.button_search = QPushButton("天気を取得")
        self.button_search.setFont(QFont("Arial", 14))
        self.button_search.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #388E3C;
                color: white;
            }
        """)
        self.button_search.clicked.connect(self.fetch_weather)
        main_layout.addWidget(self.button_search, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.update_city_selector()

    def update_city_selector(self):
        """ 都道府県選択に応じて市町村選択を更新 """
        prefecture = self.prefecture_selector.currentText()
        cities = prefecture_city_map.get(prefecture, [])
        self.city_selector.clear()
        self.city_selector.addItems(cities)

    def fetch_weather(self):
        """ 天気情報を取得して表示 """
        city_name_jp = self.city_selector.currentText()
        city_name_en = city_name_map.get(city_name_jp, "")

        # 現在の天気
        weather = get_weather(city_name_en)
        if weather:
            self.label_weather.setText(f"{weather['city']} の天気\n"
                                       f"気温: {weather['temperature']}°C\n"
                                       f"{weather['description']}")
            update_weather_icon(self.weather_icon, weather["icon"])
        else:
            self.label_weather.setText("天気情報を取得できませんでした。")

        # 週間天気
        forecast = get_forecast(city_name_en)
        if forecast:
            forecast_text = "週間天気予報:\n"
            for date, info in forecast.items():
                forecast_text += f"{date}: {info['temp_min']}°C - {info['temp_max']}°C, {info['description']}\n"
            self.label_forecast.setText(forecast_text)
        else:
            self.label_forecast.setText("週間天気を取得できませんでした。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())