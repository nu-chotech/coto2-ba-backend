from fastapi import APIRouter, HTTPException

from app.schemas.vector import CalcRequest, CalcResponse, InitResponse
from app.services.vector_engine import VectorEngine

router = APIRouter(prefix="/vector", tags=["vector"])

# word2vecモデルのロードは重いため、起動時に1回だけ初期化する
engine = VectorEngine()


@router.get("/health")
def health():
    """Vector機能の死活確認"""
    return {"status": "ok"}


@router.get("/init", response_model=InitResponse)
def init():
    """
    ゲーム開始時に最初のワードをランダムで返す。
    リクエストはパラメータなしのGETのみ。
    """
    return engine.get_start_word()


@router.post("/calc", response_model=CalcResponse)
def calc(req: CalcRequest):
    """
    ワードのベクトルを混合し、結果ワード・ランク・ヒントを返す。
    input_word が辞書に存在しない場合は 422 エラーを返す。
    """
    try:
        return engine.calc(req)
    except KeyError:
        raise HTTPException(
            status_code=422,
            detail=f"「{req.input_word}」は辞書に存在しないワードです。別のワードを試してください。",
        )
