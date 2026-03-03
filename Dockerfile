# ── Stage 1: ビルド ──────────────────────────────────
FROM python:3.11-slim AS builder

# uv をインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 依存関係のインストール（キャッシュ効率のために先にコピー）
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project

# アプリケーションコードをコピー
COPY app/ ./app/

# ── Stage 2: ランタイム ──────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# ビルド済みの仮想環境とアプリをコピー
COPY --from=builder /app /app

# モデルディレクトリを作成（ボリュームマウント用）
RUN mkdir -p /app/app/models

# ダウンロードスクリプトをコピー
COPY scripts/download_model.sh /app/scripts/download_model.sh
RUN chmod +x /app/scripts/download_model.sh

# エントリポイントスクリプトをコピー
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh

# curl（ヘルスチェック・DL用）と bzip2（モデル解凍用）をインストール
RUN apt-get update && apt-get install -y --no-install-recommends curl bzip2 && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
