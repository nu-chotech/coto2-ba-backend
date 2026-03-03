# Coto2-Ba Backend

単語のベクトル演算を用いた言葉パズルゲーム **Coto2-Ba** のバックエンド API です。  
[FastAPI](https://fastapi.tiangolo.com/) + [gensim](https://radimrehurek.com/gensim/) で構築され、Wikipedia 学習済み word2vec モデル（[WikiEntVec](https://github.com/singletongue/WikiEntVec)）を利用して単語の混合・近傍検索・ヒント生成を行います。

## 技術スタック

| カテゴリ           | ツール                |
| ------------------ | --------------------- |
| 言語               | Python 3.11+          |
| Web フレームワーク | FastAPI               |
| ベクトル演算       | gensim (KeyedVectors) |
| 単語説明           | Wikipedia API         |
| パッケージ管理     | uv                    |
| リンター           | Ruff                  |
| タスクランナー     | taskipy               |
| デプロイ           | Render / Docker       |

## ディレクトリ構成

```
.
├── pyproject.toml          # プロジェクト設定・依存関係
├── render.yaml             # Render デプロイ設定
├── Dockerfile              # Docker イメージ定義
├── docker-compose.yml      # オンプレミス Docker Compose 構成
├── scripts/
│   ├── download_model.sh   # モデル自動ダウンロードスクリプト
│   └── entrypoint.sh       # コンテナ起動エントリポイント
└── app/
    ├── main.py             # FastAPI アプリケーション本体
    ├── dependencies.py     # 共通ミドルウェア（認証等の雛形）
    ├── models/             # word2vec モデルファイル置き場
    │   └── jawiki.word_vectors.200d.txt
    ├── routers/
    │   └── vector.py       # /vector エンドポイント定義
    ├── schemas/
    │   └── vector.py       # リクエスト / レスポンスの Pydantic モデル
    └── services/
        └── vector_engine.py  # ベクトル演算のコアロジック
```

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/nu-chotech/coto2-ba-backend.git
cd coto2-ba-backend
```

### 2. 依存パッケージのインストール

[uv](https://docs.astral.sh/uv/) を使用します。

```bash
uv sync
```

### 3. word2vec モデルのダウンロード

WikiEntVec の学習済みモデル（200 次元、圧縮時約 588 MB）をダウンロードし、解凍します。

```bash
cd app/models

# ダウンロード
wget https://github.com/singletongue/WikiEntVec/releases/download/20190520/jawiki.word_vectors.200d.txt.bz2

# 解凍（解凍後は jawiki.word_vectors.200d.txt になります）
bzip2 -d jawiki.word_vectors.200d.txt.bz2

cd ../..
```

### 4. 開発サーバーの起動

```bash
uv run task dev
```

サーバーが起動したら http://localhost:8000/docs で Swagger UI を確認できます。

## タスク一覧

| コマンド            | 説明                                     |
| ------------------- | ---------------------------------------- |
| `uv run task dev`   | 開発サーバーを起動（ホットリロード有効） |
| `uv run task start` | 本番用サーバーを起動                     |
| `uv run task lint`  | Ruff によるリントチェック                |

## API エンドポイント

### `GET /`

死活確認用。Render のヘルスチェックにも使用されます。

### `GET /vector/health`

Vector 機能の死活確認。

### `POST /vector/init`

ゲーム開始時に最初のワードをランダムで返します。

**リクエスト**

```json
{
  "goal_word": "100億"
}
```

**レスポンス**

```json
{
  "start_word": "宇宙",
  "rank": 12345,
  "description": "宇宙とは、…"
}
```

### `POST /vector/calc`

現在のワードとユーザー入力ワードをベクトル混合し、結果ワード・ランク・ヒントを返します。

**リクエスト**

```json
{
  "goal_word": "100億",
  "current_word": "宇宙",
  "input_word": "投資",
  "mix_ratio": 0.5
}
```

**レスポンス**

```json
{
  "new_word": "資産",
  "rank": 5678,
  "hint_words": ["経済", "銀行", "金融", "市場", "企業", "資本"],
  "description": "資産とは、…"
}
```

## デプロイ

### Render（クラウド）

本番環境は [Render](https://render.com/) にデプロイされています。設定は [render.yaml](render.yaml) を参照してください。

### Docker Compose（オンプレミス）

Docker Compose を使ってオンプレミス環境にデプロイできます。
初回起動時に [WikiEntVec](https://github.com/singletongue/WikiEntVec) の学習済みモデル（約 588 MB、解凍後約 1.6 GB）を自動ダウンロードします。

#### 前提条件

- Docker Engine 20.10+
- Docker Compose v2+
- メモリ 4GB 以上

#### 手順

```bash
# ビルド & 起動（初回はモデル DL に数分かかります）
docker compose up -d --build

# ログを確認
docker compose logs -f
```

ダウンロード済みのモデルは名前付きボリュームに永続化されるため、2回目以降はダウンロードをスキップします。

#### 運用コマンド

```bash
# 停止
docker compose down

# 停止 & モデルデータも削除
docker compose down -v

# 再ビルド（コード変更後）
docker compose up -d --build

# ヘルスチェック
curl http://localhost:8000/
```

## ライセンス

本リポジトリのライセンスは未定です。
