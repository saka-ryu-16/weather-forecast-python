import requests

areas = {
    "北海道": (43.0642, 141.3469),
    "青森県": (40.8244, 140.7400),
    "岩手県": (39.7036, 141.1527),
    "宮城県": (38.2682, 140.8694),
    "秋田県": (39.7186, 140.1024),
    "山形県": (38.2404, 140.3633),
    "福島県": (37.7503, 140.4676),

    "茨城県": (36.3418, 140.4468),
    "栃木県": (36.5657, 139.8836),
    "群馬県": (36.3911, 139.0608),
    "埼玉県": (35.8617, 139.6455),
    "千葉県": (35.6074, 140.1065),
    "東京都": (35.6895, 139.6917),
    "神奈川県": (35.4478, 139.6425),

    "新潟県": (37.9024, 139.0232),
    "富山県": (36.6953, 137.2113),
    "石川県": (36.5947, 136.6256),
    "福井県": (36.0652, 136.2216),
    "山梨県": (35.6642, 138.5684),
    "長野県": (36.6513, 138.1810),
    "岐阜県": (35.3912, 136.7223),
    "静岡県": (34.9769, 138.3831),
    "愛知県": (35.1802, 136.9066),

    "三重県": (34.7303, 136.5086),
    "滋賀県": (35.0045, 135.8686),
    "京都府": (35.0116, 135.7681),
    "大阪府": (34.6937, 135.5023),
    "兵庫県": (34.6901, 135.1955),
    "奈良県": (34.6851, 135.8048),
    "和歌山県": (34.2260, 135.1675),

    "鳥取県": (35.5039, 134.2377),
    "島根県": (35.4723, 133.0505),
    "岡山県": (34.6618, 133.9350),
    "広島県": (34.3966, 132.4596),
    "山口県": (34.1861, 131.4705),

    "徳島県": (34.0658, 134.5593),
    "香川県": (34.3401, 134.0434),
    "愛媛県": (33.8416, 132.7661),
    "高知県": (33.5597, 133.5311),

    "福岡県": (33.5904, 130.4017),
    "佐賀県": (33.2635, 130.3009),
    "長崎県": (32.7448, 129.8737),
    "熊本県": (32.7898, 130.7417),
    "大分県": (33.2382, 131.6126),
    "宮崎県": (31.9111, 131.4239),
    "鹿児島県": (31.5602, 130.5581),
    "沖縄県": (26.2124, 127.6809),
}


area=input("""
どこの都道府県の天気予報が知りたいですか？
都道府県名を書いてください(例:東京都・大阪府・北海道・愛知県...)

           """)


while area not in areas:
    area=input("""
都道府県名が正しく入力されていません
どこの都道府県の天気予報が知りたいですか？
都道府県名を書いてください(例:東京都・大阪府・北海道・愛知県...)

        """)     
if area in areas:
    latitude,longitude=areas[area]

url="https://api.open-meteo.com/v1/forecast"

headers={
    "Accept":"application/json",
    "Accept-Language":"ja"
}
params={
    "latitude":latitude,
    "longitude":longitude,
    "hourly":["temperature_2m","weather_code"],
    "daily":["temperature_2m_max","temperature_2m_min","weather_code"],
    "timezone":"Asia/Tokyo"    
}

try:
    response=requests.get(url, headers=headers, timeout=10, params=params)
    response.raise_for_status()
except Exception as e:
    print("接続できませんでした")
    raise
    
data=response.json()

daily=data["daily"]
dates=daily["time"]
max_temp=daily["temperature_2m_max"]
min_temp=daily["temperature_2m_min"]
weather_date=daily["weather_code"]
hour=data["hourly"]
hour_temp=hour["temperature_2m"]
hour_weather=hour["weather_code"]
hour_time=hour["time"]

weather_list={
    0:"快晴",
    1:"晴れ",
    2:"晴れ時々くもり",
    3:"くもり",
    45:"霧",
    48:"濃い霧",
    51:"霧雨",
    53:"やや強い霧雨",
    55:"強い霧雨",
    56:"冷たい霧雨",
    57:"冷たくて強い霧雨",
    61:"弱い雨",
    63:"雨",
    65:"強い雨",
    66:"みぞれ",
    67:"強いみぞれ",
    71:"弱い雪",
    73:"雪",
    75:"大雪",
    77:"あられ",
    80:"にわか雨",
    81:"強いにわか雨",
    82:"激しいにわか雨",
    85:"にわか雪",
    86:"にわか雪",
    95:"雷雨",
    96:"ひょうを伴う雷雨",
    99:"激しいひょうを伴う雷雨"
}

def days_temp_weather():
    for d_time,ma_temp,mi_temp,d_weather in zip(dates,max_temp,min_temp,weather_date):
        weather_text_d=weather_list.get(d_weather,"不明")
        print(f"""
==== {d_time} ====
最高気温:{ma_temp}°C
最低気温:{mi_temp}°C
天気:{weather_text_d}
""")
        for h_time,h_temp,h_weather in zip(hour_time,hour_temp,hour_weather):
            date_part,hour_part=h_time.split("T")
            if date_part==d_time:
                    weather_text_h=weather_list.get(h_weather,"不明")
                    print(f"{hour_part} {h_temp}°C{weather_text_h}")
days_temp_weather()