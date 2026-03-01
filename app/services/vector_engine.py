from app.schemas.vector import CalcRequest, CalcResponse

# TODO: word2vec モデルのロード（gensim を使う予定）
# from gensim.models import KeyedVectors
# model = KeyedVectors.load("models/word2vec.bin")

NG_WORDS = {"億", "万", "数字", "お金", "金", "円", "富"}


class VectorEngine:
    """
    ベクトル演算のコアクラス。
    現時点はスタブ（仮の実装）。
    word2vec の組み込みは別途行う。
    """

    def __init__(self):
        # TODO: word2vec モデルをここでロードする
        # self.model = KeyedVectors.load("models/word2vec.bin")
        # self.target_vector = self.model["100億"]
        pass

    def calc(self, req: CalcRequest) -> CalcResponse:
        # NGワードチェック
        if req.input_word in NG_WORDS:
            return CalcResponse(
                new_word="（ペナルティ）",
                new_vector=req.current_vector,
                sync_rate=0.0,
                is_ng_word=True,
            )

        # TODO: 実際のベクトル演算に置き換える
        # input_vec = self.model[req.input_word]
        # new_vec = current + input_vec  if add  else  current - input_vec
        # new_word = self.model.similar_by_vector(new_vec, topn=1)[0][0]
        # sync_rate = cosine_similarity(new_vec, self.target_vector) * 100

        # ── スタブ：常にダミーの値を返す ──
        dummy_vector = [0.1] * 300  # word2vec は通常300次元
        return CalcResponse(
            new_word=f"（スタブ）{req.input_word}の結果",
            new_vector=dummy_vector,
            sync_rate=42.0,  # ダミーのシンクロ率
            is_ng_word=False,
        )
