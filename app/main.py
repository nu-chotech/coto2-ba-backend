from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import vector

app = FastAPI(
    title="Coto2-Ba API",
    description="単語のベクトル演算を行うAPI",
    version="0.1.0",
)

# CORS設定（フロントエンドからのリクエストを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # ローカル開発用
        "https://coto2-ba.vercel.app",  # 本番フロントエンド（後で変更）
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(vector.router)


@app.get("/")
def root():
    """死活確認用。Renderのヘルスチェックにも使われる"""
    return {"status": "ok", "message": "Coto2-Ba API is running 🚀"}
