import random

from app.schemas.vector import CalcRequest, CalcResponse, InitResponse

# TODO: word2vec モデルのロード
# import numpy as np
# from gensim.models import KeyedVectors
# model = KeyedVectors.load_word2vec_format("models/word2vec.bin", binary=True)

# スタート候補ワード（本実装では word2vec の語彙からランダム抽出に置き換える）
START_WORD_CANDIDATES = [
    ("ミジンコ", "非常に小さな甲殻類の一種。池や沼に生息する。"),
    ("ふきのとう", "フキの若い芽。春の山菜として親しまれる。"),
    ("そろばん", "計算に用いる伝統的な道具。玉を弾いて数を表す。"),
]


class VectorEngine:
    """
    ベクトル演算のコアクラス。
    現時点はスタブ（仮の実装）。
    word2vec の組み込みは別途行う。
    """

    def __init__(self):
        # TODO: word2vec モデルをロードする
        # self.model = KeyedVectors.load_word2vec_format("models/word2vec.bin", binary=True)
        pass

    def get_start_word(self) -> InitResponse:
        """
        ゲームの開始ワードをランダムで返す。
        本実装では word2vec の語彙からランダム抽出する。
        """
        # TODO: self.model.index_to_key からランダム抽出に置き換える
        word, description = random.choice(START_WORD_CANDIDATES)
        return InitResponse(start_word=word, description=description)

    def calc(self, req: CalcRequest) -> CalcResponse:
        """
        current_word と input_word を mix_ratio で混合し、
        最も近い new_word・ランク・ヒントワードを返す。
        input_word が辞書にない場合は KeyError を raise する（router でキャッチ）。
        """
        # TODO: 実装例（gensim を使った場合）
        #
        # if req.input_word not in self.model:
        #     raise KeyError(req.input_word)   # router 側で 422 エラーにする
        #
        # vec_current = self.model[req.current_word]
        # vec_input   = self.model[req.input_word]
        # vec_goal    = self.model[req.goal_word]
        #
        # # mix_ratio で混合（1.0 なら input_word 100%、0.0 なら current_word 100%）
        # vec_new = (1 - req.mix_ratio) * vec_current + req.mix_ratio * vec_input
        #
        # # 混合ベクトルに最も近いワードを取得
        # similar = self.model.similar_by_vector(vec_new, topn=20)
        # new_word = similar[0][0]
        #
        # # goal_word に近いワードのランキング順位を取得
        # neighbors = self.model.similar_by_vector(vec_goal, topn=500)
        # rank_map  = {w: i for i, (w, _) in enumerate(neighbors)}
        # rank      = rank_map.get(new_word, 999)
        #
        # # ヒントワード：goal_word と new_word の中間ベクトル付近の語を提案
        # hint_words = [w for w, _ in self.model.similar_by_vector(
        #     (vec_new + vec_goal) / 2, topn=8
        # ) if w != new_word][:6]
        #
        # description = f"「{new_word}」の説明（辞書APIと連携予定）"
        #
        # return CalcResponse(
        #     new_word=new_word,
        #     rank=rank,
        #     hint_words=hint_words,
        #     description=description,
        # )

        # ── スタブ：ダミーの値を返す ────────────────────────
        # input_word が "error" のときだけ KeyError を再現できるようにしておく（テスト用）
        if req.input_word == "error":
            raise KeyError(req.input_word)

        return CalcResponse(
            new_word=f"（スタブ）{req.input_word} × {req.mix_ratio}",
            rank=42,
            hint_words=[
                "ヒント1",
                "ヒント2",
                "ヒント3",
                "ヒント4",
                "ヒント5",
                "ヒント6",
            ],
            description=f"「{req.input_word}」を混合した結果のワードです。（スタブ）",
        )
