from pydantic import BaseModel, Field


# ── /init ──────────────────────────────────────────────
class InitRequest(BaseModel):
    """ゲーム開始時のリクエスト"""

    goal_word: str  # ゲームの目標ワード


class InitResponse(BaseModel):
    """ゲーム開始時のレスポンス"""

    start_word: str  # ゲームの最初のワード
    rank: int  # 目標ワードとの近さランキング（0以上、小さいほど近い）
    description: str  # 単語の意味・説明


# ── /calc ──────────────────────────────────────────────
class CalcRequest(BaseModel):
    """ベクトル計算リクエスト"""

    goal_word: str  # 目標ワード（例: "100億"）
    current_word: str  # 現在のワード
    input_word: str  # ユーザーが入力した単語
    mix_ratio: float = Field(ge=0.0, le=1.0)  # 混合比率（0.0〜1.0）


class CalcResponse(BaseModel):
    """ベクトル計算レスポンス"""

    new_word: str  # 計算結果のワード
    rank: int  # 目標ワードとの近さランキング（0以上、小さいほど近い）
    hint_words: list[str]  # 次に試すべきおすすめワード候補6件
    description: str  # new_word の説明
