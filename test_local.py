#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ローカル環境でテストするためのスクリプト
.env ファイルから環境変数を読み込んで weather_bot.py を実行します
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  python-dotenv がインストールされていません。")
    print("以下のコマンドでインストールしてください：")
    print("  pip install python-dotenv")
    exit(1)

# .env ファイルを読み込む
env_path = Path(__file__).parent / '.env'

if not env_path.exists():
    print("❌ .env ファイルが見つかりません。")
    print(".env.example をコピーして .env を作成し、必要な値を設定してください：")
    print("  cp .env.example .env")
    exit(1)

load_dotenv(env_path)

# 必要な環境変数がすべて設定されているか確認
required_vars = ['OWM_API_KEY', 'LATITUDE', 'LONGITUDE', 'DISCORD_WEBHOOK_URL']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"❌ 以下の環境変数が設定されていません: {', '.join(missing_vars)}")
    print(".env ファイルを確認してください。")
    exit(1)

print("✅ 環境変数の読み込みが完了しました。")
print("🚀 weather_bot.py を実行します...\n")

# weather_bot.py を実行
import weather_bot
weather_bot.main()
