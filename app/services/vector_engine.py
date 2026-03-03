from __future__ import annotations

import random

import numpy as np
import wikipedia  # type: ignore[import-untyped]
from gensim.models import KeyedVectors  # type: ignore[import-untyped]

from app.schemas.vector import (CalcRequest, CalcResponse, InitRequest,
                                InitResponse)

# Wikipediaの言語設定
wikipedia.set_lang("ja")  # type: ignore[no-untyped-call]

# スタート候補ワード
START_WORD_CANDIDATES: list[str] = [
    "投資",
    "学校",
    "宇宙",
    "魔法",
    "侍",
    "コンピュータ",
    "恋愛",
    "筋肉",
    "インターネット",
    "時間",
    "料理",
    "人工知能",
    "地球",
    "歴史",
    "音楽",
    "スポーツ",
]

MODEL_PATH = "app/models/jawiki.word_vectors.200d.txt"


class VectorEngine:
    """word2vec を用いたベクトル演算のコアクラス。"""

    model: KeyedVectors

    def __init__(self) -> None:
        self.model = KeyedVectors.load_word2vec_format(MODEL_PATH, binary=False)

    # ── ユーティリティ ─────────────────────────────────

    def get_wikipedia_summary(self, word: str) -> str:
        """Wikipedia から単語の概要を1文だけ取得する。"""
        try:
            search_results: list[str] = wikipedia.search(word)  # type: ignore[no-untyped-call]
            if not search_results:
                return "未知の概念です。"
            summary: str = wikipedia.summary(  # type: ignore[no-untyped-call]
                search_results[0], sentences=1
            )
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            options: list[str] = e.options[:3]  # type: ignore[union-attr]
            return f"複数の意味があります（例: {', '.join(options)} など）"
        except Exception:
            return "辞書に載っていませんでした。"

    def _rank(self, goal_word: str, word: str) -> int:
        """goal_word から見た word の順位を返す。算出不能なら 0。"""
        if goal_word in self.model.key_to_index and word in self.model.key_to_index:
            rank: int = self.model.rank(goal_word, word)
            return rank
        return 0

    # ── エンドポイント向けメソッド ─────────────────────

    def get_start_word(self, req: InitRequest) -> InitResponse:
        """
        START_WORD_CANDIDATES からゲームの開始ワードをランダムで返す。
        """
        word = random.choice(START_WORD_CANDIDATES)
        description = self.get_wikipedia_summary(word)
        rank = self._rank(req.goal_word, word)

        return InitResponse(
            start_word=word,
            rank=rank,
            description=description,
        )

    def calc(self, req: CalcRequest) -> CalcResponse:
        """
        current_word と input_word を mix_ratio で混合し、
        最も近い new_word・ランク・ヒントワードを返す。
        辞書にない単語が含まれる場合は ValueError を raise する。
        """
        self._validate_words(req)

        # ベクトル合成
        v_new: np.ndarray = (1.0 - req.mix_ratio) * self.model[
            req.current_word
        ] + req.mix_ratio * self.model[req.input_word]

        # 近傍単語の抽出（current / input 自身は除外）
        new_word = self._nearest_word(v_new, exclude={req.current_word, req.input_word})

        # ランク判定
        rank = self._rank(req.goal_word, new_word)

        # ヒントの取得
        hint_words = self._build_hint_words(req, new_word)

        description = self.get_wikipedia_summary(new_word)

        return CalcResponse(
            new_word=new_word,
            rank=rank,
            hint_words=hint_words,
            description=description,
        )

    # ── プライベートヘルパー ───────────────────────────

    def _validate_words(self, req: CalcRequest) -> None:
        """リクエスト中の単語がすべて語彙に存在するか検証する。"""
        if req.current_word not in self.model.key_to_index:
            raise ValueError(f"「{req.current_word}」は辞書にありません。")
        if req.input_word not in self.model.key_to_index:
            raise ValueError(f"「{req.input_word}」は辞書にありません。")
        if req.goal_word not in self.model.key_to_index:
            raise ValueError(f"ゴール「{req.goal_word}」が辞書にありません。")

    def _nearest_word(
        self,
        vector: np.ndarray,
        *,
        exclude: set[str],
        topn: int = 10,
    ) -> str:
        """vector に最も近い単語を返す。exclude に含まれる単語はスキップする。"""
        candidates: list[tuple[str, float]] = self.model.similar_by_vector(
            vector, topn=topn
        )
        for word, _sim in candidates:
            if word not in exclude:
                return str(word)

        return str(candidates[0][0]) if candidates else ""

    def _build_hint_words(
        self,
        req: CalcRequest,
        new_word: str,
        *,
        hint_count: int = 6,
        hint_ratio: float = 0.2,
    ) -> list[str]:
        """
        new_word をベースに goal_word 方向へ少し寄せたベクトルから
        ヒントワードを最大 hint_count 個返す。
        hint_ratio でヒントの露骨さ（難易度）を調整できる。
        """
        if (
            new_word not in self.model.key_to_index
            or req.goal_word not in self.model.key_to_index
        ):
            return []

        v_hint: np.ndarray = (1.0 - hint_ratio) * self.model[
            new_word
        ] + hint_ratio * self.model[req.goal_word]
        raw_hints: list[tuple[str, float]] = self.model.similar_by_vector(
            v_hint, topn=100
        )

        forbidden = {req.current_word, req.input_word, new_word, req.goal_word}
        hint_words: list[str] = []
        for w, _sim in raw_hints:
            if w not in forbidden:
                hint_words.append(str(w))
                if len(hint_words) >= hint_count:
                    break
        return hint_words
