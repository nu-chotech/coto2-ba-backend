from fastapi import APIRouter, HTTPException

from app.schemas.vector import CalcRequest, CalcResponse, InitRequest, InitResponse
from app.services.vector_engine import VectorEngine

router = APIRouter(prefix="/vector", tags=["vector"])

# word2vecモデルのロードは重いため、起動時に1回だけ初期化する
engine = VectorEngine()


@router.get("/health")
def health():
    """Vector機能の死活確認"""
    return {"status": "ok"}


@router.post("/init", response_model=InitResponse)
def init(req: InitRequest):
    """
    ゲーム開始時に最初のワードをランダムで返す。
    """
    return engine.get_start_word(req)


@router.post("/calc", response_model=CalcResponse)
def calc(req: CalcRequest):
    """
    ワードのベクトルを混合し、結果ワード・ランク・ヒントを返す。
    input_word が辞書に存在しない場合は 422 エラーを返す。
    """
    try:
        return engine.calc(req)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )
