#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenWeather API を使用して気象情報を取得し、Discord Webhook に送信するスクリプト
改善版：コンパクトで見やすいフォーマット
"""

import os
import requests
from datetime import datetime, timedelta
import pytz

# 環境変数から取得
API_KEY = os.environ.get('OWM_API_KEY')
LAT = os.environ.get('LATITUDE')
LON = os.environ.get('LONGITUDE')
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# 日本時間のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')


def get_weather_emoji(weather_id):
    """天気IDから絵文字を返す"""
    if 200 <= weather_id < 300:
        return "⛈️"
    elif 300 <= weather_id < 400:
        return "🌦️"
    elif 500 <= weather_id < 600:
        return "🌧️"
    elif 600 <= weather_id < 700:
        return "❄️"
    elif 700 <= weather_id < 800:
        return "🌫️"
    elif weather_id == 800:
        return "☀️"
    elif weather_id == 801:
        return "🌤️"
    elif weather_id == 802:
        return "⛅"
    elif weather_id in [803, 804]:
        return "☁️"
    else:
        return "🌡️"


def fetch_weather_data():
    """OpenWeather API から5日間の天気予報を取得"""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat': LAT,
        'lon': LON,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ja'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def parse_hourly_data(data_list, target_date):
    """特定の日付の時間ごとデータを抽出"""
    hourly_info = []
    
    for item in data_list:
        dt = datetime.fromtimestamp(item['dt'], tz=JST)
        
        if dt.date() == target_date:
            hourly_info.append({
                'time': dt.strftime('%H:%M'),
                'temp': round(item['main']['temp'], 1),
                'weather': item['weather'][0]['description'],
                'weather_id': item['weather'][0]['id'],
                'humidity': item['main']['humidity'],
                'wind_speed': round(item['wind']['speed'], 1)
            })
    
    return hourly_info


def parse_daily_summary(data_list):
    """5日間の日次サマリーを作成"""
    daily_data = {}
    
    for item in data_list:
        dt = datetime.fromtimestamp(item['dt'], tz=JST)
        date_key = dt.date()
        
        if date_key not in daily_data:
            daily_data[date_key] = {
                'temps': [],
                'weather_ids': [],
                'weathers': []
            }
        
        daily_data[date_key]['temps'].append(item['main']['temp'])
        daily_data[date_key]['weather_ids'].append(item['weather'][0]['id'])
        daily_data[date_key]['weathers'].append(item['weather'][0]['description'])
    
    # 各日のサマリーを作成
    summary = []
    for date, info in sorted(daily_data.items())[:5]:
        most_common_weather_id = max(set(info['weather_ids']), key=info['weather_ids'].count)
        most_common_weather = info['weathers'][info['weather_ids'].index(most_common_weather_id)]
        
        summary.append({
            'date': date.strftime('%m/%d (%a)'),
            'temp_min': round(min(info['temps']), 1),
            'temp_max': round(max(info['temps']), 1),
            'weather': most_common_weather,
            'weather_id': most_common_weather_id
        })
    
    return summary


def format_hourly_compact(hourly_data, max_hours=6):
    """時間ごとデータをコンパクトに整形（1行形式）"""
    if not hourly_data:
        return "データなし"
    
    lines = []
    for hour in hourly_data[:max_hours]:
        emoji = get_weather_emoji(hour['weather_id'])
        # 1行にまとめる
        line = f"**{hour['time']}** {emoji} {hour['temp']}°C 💧{hour['humidity']}% 💨{hour['wind_speed']}m/s"
        lines.append(line)
    
    return "\n".join(lines)


def create_discord_embed(weather_data):
    """Discord用のEmbedメッセージを作成（改善版）"""
    now = datetime.now(JST)
    today = now.date()
    tomorrow = today + timedelta(days=1)
    
    # 時間ごとデータを取得
    today_hourly = parse_hourly_data(weather_data['list'], today)
    tomorrow_hourly = parse_hourly_data(weather_data['list'], tomorrow)
    
    # 5日間サマリー
    daily_summary = parse_daily_summary(weather_data['list'])
    
    # 都市名を取得
    city_name = weather_data.get('city', {}).get('name', '不明')
    
    # Embedの作成
    embed = {
        "title": "☀️ 今日の天気予報",
        "description": f"**{today.strftime('%Y年%m月%d日 (%A)')}** | {city_name}",
        "color": 3447003,
        "fields": [],
        "footer": {
            "text": "OpenWeather API | 毎朝5時更新"
        },
        "timestamp": now.isoformat()
    }
    
    # 今日の天気（コンパクト版）
    if today_hourly:
        today_text = format_hourly_compact(today_hourly, max_hours=6)
        embed["fields"].append({
            "name": "📅 今日の天気（時間ごと）",
            "value": today_text,
            "inline": False
        })
    
    # 明日の天気（コンパクト版）
    if tomorrow_hourly:
        tomorrow_text = format_hourly_compact(tomorrow_hourly, max_hours=6)
        embed["fields"].append({
            "name": f"📅 明日の天気 - {tomorrow.strftime('%m/%d (%a)')}",
            "value": tomorrow_text,
            "inline": False
        })
    
    # 5日間の概要（よりコンパクトに）
    if daily_summary:
        summary_lines = []
        for day in daily_summary:
            emoji = get_weather_emoji(day['weather_id'])
            summary_lines.append(
                f"**{day['date']}** {emoji} {day['temp_min']}°C〜{day['temp_max']}°C {day['weather']}"
            )
        
        embed["fields"].append({
            "name": "📊 5日間の天気予報",
            "value": "\n".join(summary_lines),
            "inline": False
        })
    
    return embed


def send_to_discord(embed):
    """Discord Webhookにメッセージを送信"""
    payload = {
        "embeds": [embed],
        "username": "お天気ボット"
    }
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print("✅ Discord への送信が完了しました！")


def main():
    """メイン処理"""
    try:
        # 環境変数のチェック
        if not all([API_KEY, LAT, LON, DISCORD_WEBHOOK_URL]):
            raise ValueError("必要な環境変数が設定されていません")
        
        print("🌍 天気データを取得中...")
        weather_data = fetch_weather_data()
        
        print("📝 メッセージを作成中...")
        embed = create_discord_embed(weather_data)
        
        print("📤 Discord に送信中...")
        send_to_discord(embed)
        
        print("🎉 処理が完了しました！")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        raise


if __name__ == "__main__":
    main()
