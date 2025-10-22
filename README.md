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
