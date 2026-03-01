from fastapi import APIRouter
from app.schemas.vector import CalcRequest, CalcResponse
from app.services.vector_engine import VectorEngine

router = APIRouter(prefix="/vector", tags=["vector"])

# アプリ起動時にVectorEngineを1回だけ初期化（word2vecモデルのロードは重いため）
engine = VectorEngine()


@router.get("/health")
def health():
    """Vector機能の死活確認"""
    return {"status": "ok"}


@router.post("/calc", response_model=CalcResponse)
def calc(req: CalcRequest):
    """
    単語のベクトル演算を行い、結果の単語とシンクロ率を返す。
    ロジックは VectorEngine に委譲する。
    """
    return engine.calc(req)
