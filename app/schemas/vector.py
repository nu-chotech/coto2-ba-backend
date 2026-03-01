from pydantic import BaseModel
from typing import Literal


class CalcRequest(BaseModel):
    """演算リクエストの型"""
    current_vector: list[float]  # 現在の単語のベクトル
    input_word: str              # ユーザーが入力した単語
    operation: Literal["add", "subtract"]  # 足す or 引く


class CalcResponse(BaseModel):
    """演算レスポンスの型"""
    new_word: str          # 演算結果に最も近い日本語単語
    new_vector: list[float]  # 演算後のベクトル
    sync_rate: float       # 100億とのシンクロ率（0〜100）
    is_ng_word: bool       # NGワードだったか
