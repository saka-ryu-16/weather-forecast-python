import requests

url="https://api.open-meteo.com/v1/forecast"

from datetime import datetime,timedelta

latitude=35.6895
longitude=139.6917


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
    x=0
    while x<len(dates):
        start_date=dates[x]
        start_temp=max_temp[x]
        start_weather=weather_date[x]
        weather_text=weather_list.get(start_weather,"不明")
        print(f"{start_date}日の最高気温は{start_temp}度で天気は{weather_text}です")
        x+=1
    for time,temp,weather  in zip(hour_time,hour_temp,hour_weather):
        weather_text=weather_list.get(weather,"不明")
        print(f"{time}時の気温は{temp}で天気は{weather_text}です")
days_temp_weather()