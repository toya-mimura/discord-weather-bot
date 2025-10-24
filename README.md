# 🌤️ Discord天気予報ボット

OpenWeather APIを使用して、毎朝5時（日本時間）にDiscordへ天気予報を自動配信するボットです。

## ✨ 機能

- 📅 **今日の天気**：時間ごとの気温、湿度、風速、天候
- 📅 **明日の天気**：時間ごとの気温、湿度、風速、天候
- 📊 **5日間予報**：各日の最高/最低気温と天候
- 🤖 **自動配信**：GitHub Actionsで毎朝自動実行
- 🌐 **日本語対応**：すべての情報が日本語で表示

## 📋 必要なもの

1. **OpenWeather APIキー**
   - [OpenWeatherMap](https://openweathermap.org/api)で無料アカウントを作成
   - APIキーを取得（Free tierで十分です）
   - APIキーの取得の仕方は[こちら](https://toyaworks.substack.com/i/172839771/openweatherowmについて)に記事を書いておきました

2. **Discord Webhook URL**
   - Discordサーバーの設定から「連携サービス」→「ウェブフック」を作成
   - Webhook URLをコピー

3. **GitHubアカウント**
   - Publicリポジトリを作成（GitHub Actionsの無料枠を使用）

## 🚀 セットアップ手順

### 1. リポジトリの準備
```bash
# このリポジトリをfork、またはファイルをコピー
git clone <your-repository-url>
cd <repository-name>
```

### 2. GitHub Secretsの設定

リポジトリの `Settings` → `Secrets and variables` → `Actions` で以下のSecretsを追加：

| Secret名 | 説明 | 例 |
|---------|------|-----|
| `OWM_API_KEY` | OpenWeather APIキー | `abc123def456...` |
| `LATITUDE` | 取得したい地点の緯度 | `35.6762` (東京の場合) |
| `LONGITUDE` | 取得したい地点の経度 | `139.6503` (東京の場合) |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | `https://discord.com/api/webhooks/...` |

#### 📍 緯度・経度の調べ方

- [Google Maps](https://www.google.com/maps)で場所を右クリック→座標をコピー
- または [LatLong.net](https://www.latlong.net/)を使用

### 3. ファイルのアップロード

以下のファイルをリポジトリにプッシュ：
```
├── .github/
│   └── workflows/
│       └── weather-notification.yml
├── .gitignore
├── weather_bot.py
├── requirements.txt
└── README.md
```

```bash
git add .
git commit -m "Initial commit: Weather bot setup"
git push origin main
```

### 4. 動作確認

#### 手動実行でテスト

1. GitHubリポジトリの `Actions` タブを開く
2. `天気予報配信` ワークフローを選択
3. `Run workflow` ボタンをクリック
4. Discordチャンネルに天気予報が届くことを確認

#### 自動実行の確認

- 毎日 日本時間 AM 5:00 に自動実行されます
- 次回の実行予定は Actions タブで確認できます

## 📊 配信される情報

### 今日・明日の天気（時間ごと）
- 🌡️ **気温**：摂氏（°C）
- 💧 **湿度**：パーセント（%）
- 💨 **風速**：メートル毎秒（m/s）
- ☀️ **天候**：晴れ、曇り、雨など（絵文字付き）

### 5日間予報
- 📅 **日付**：月日と曜日
- 🌡️ **気温範囲**：最低気温 ~ 最高気温
- ☁️ **天候**：その日の代表的な天気

## 🛠️ カスタマイズ

### 配信時刻の変更

`.github/workflows/weather-notification.yml` の cron 式を編集：
```yaml
schedule:
  # 例：日本時間 AM 7:00 にする場合 (UTC 22:00)
  - cron: '0 22 * * *'
```

### 表示する時間数の変更

`weather_bot.py` の以下の部分を編集：
```python
for hour in today_hourly[:8]:  # 8を好きな数字に変更
```

### メッセージのカスタマイズ

`create_discord_embed()` 関数内で、Embedの色やテキストを自由に変更できます：
```python
embed = {
    "title": "🌤️ 今日の天気予報",  # タイトルを変更
    "color": 3447003,  # 色を変更（10進数カラーコード）
    # ...
}
```

## 🔧 トラブルシューティング

### エラー：401 Unauthorized
- OpenWeather APIキーが正しいか確認
- APIキーが有効化されているか確認（取得後、数時間かかる場合があります）

### エラー：404 Not Found (Discord)
- Discord Webhook URLが正しいか確認
- Webhookが削除されていないか確認

### 天気情報が届かない
1. Actions タブでワークフローの実行ログを確認
2. Secretsが正しく設定されているか確認
3. リポジトリがPublicになっているか確認

### 時刻がずれる
- cron式はUTC基準です
- 日本時間 (JST) = UTC + 9時間
- 例：JST 05:00 = UTC 20:00（前日）

## 📝 使用しているAPI

- **Current Weather Data API**: 現在の天気情報
- **5 Day / 3 Hour Forecast API**: 5日間・3時間ごとの予報データ

無料プラン（Free tier）で利用可能です。

## 📄 ライセンス

MIT License

## 🤝 貢献

Issue や Pull Request を歓迎します！

## 📞 サポート

問題が発生した場合は、Issueを作成してください。

---

**Enjoy your weather forecasts! 🌈**
