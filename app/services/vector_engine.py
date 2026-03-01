import random
import gensim
import wikipedia

# Wikipediaの言語設定
wikipedia.set_lang("ja")

from app.schemas.vector import CalcRequest, CalcResponse, InitResponse, InitRequest

# スタート候補ワード（本実装では word2vec の語彙からランダム抽出に置き換える）
START_WORD_CANDIDATES = [
    "投資", "学校", "宇宙", "魔法", "侍", "コンピュータ", 
    "恋愛", "筋肉", "インターネット", "時間", "料理",
    "人工知能", "地球", "歴史", "音楽", "スポーツ"
]

class VectorEngine:
    """
    ベクトル演算のコアクラス。
    現時点はスタブ（仮の実装）。
    word2vec の組み込みは別途行う。
    """

    def __init__(self):
        # word2vec モデルをロードする
        self.model = gensim.models.KeyedVectors.load_word2vec_format("app/models/jawiki.word_vectors.200d.txt", binary=False)
        pass

    def get_wikipedia_summary(self, word: str) -> str:
        try:
            search_results = wikipedia.search(word)
            if not search_results: return "未知の概念です。"
            return wikipedia.summary(search_results[0], sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"複数の意味があります（例: {', '.join(e.options[:3])} など）"
        except Exception:
            return "辞書に載っていませんでした。"
        pass

    def get_start_word(self, req: InitRequest) -> InitResponse:
            """
            START_WORD_CANDIDATESからゲームの開始ワードをランダムで返し、
            ゴールワードに対する順位（rank）を計算して付与する。
            """
            # 1. 安全なリストからランダムに1つ抽出
            word = random.choice(START_WORD_CANDIDATES)
            
            # 2. 辞書の意味を取得
            description = self.get_wikipedia_summary(word)

            # 3. ゴールワードからの順位（rank）を計算
            rank = 0
            if self.model is not None and self.req.goal_word in self.model.key_to_index and word in self.model.key_to_index:
                # goal_wordから見て、選ばれたwordが全語彙の中で何番目に近いかを取得
                rank = self.model.rank(goal_word, word)

            return InitResponse(
                start_word=word, 
                description=description, 
                rank=rank
            )

    def calc(self, req: CalcRequest) -> CalcResponse:
        """
        current_word と input_word を mix_ratio で混合し、
        最も近い new_word・ランク・ヒントワードを返す。
        input_word が辞書にない場合は KeyError を raise する（router でキャッチ）。
        """
        """2つの単語を合成し、結果の辞書を返すコア関数"""
        if self.model is None:
            raise ValueError("サーバー準備中です。")
        if req.current_word not in self.model.key_to_index:
            raise ValueError(f"「{req.current_word}」は辞書にありません。")
        if req.input_word not in self.model.key_to_index:
            raise ValueError(f"「{req.input_word}」は辞書にありません。")
        if req.goal_word not in self.model.key_to_index:
            raise ValueError(f"ゴール「{req.goal_word}」が辞書にありません。")

        # ベクトル合成
        v_new = (1.0 - req.mix_ratio) * self.model[req.current_word] + req.mix_ratio * self.model[req.input_word]

        # 近傍単語の抽出
        candidates = self.model.similar_by_vector(v_new, topn=10)
        valid_candidates = [w for w, sim in candidates if w not in [req.current_word, req.input_word]]
        new_word = valid_candidates[0] if valid_candidates else req.current_word

        # ランク判定
        rank = 0
        if self.model is not None and req.goal_word in self.model.key_to_index and new_word in self.model.key_to_index:
            # goal_wordから見て、選ばれたwordが全語彙の中で何番目に近いかを取得
            rank = self.model.rank(req.goal_word, new_word)

        # ヒントの取得
        hint_words = []
        if new_word in self.model.key_to_index and req.goal_word in self.model.key_to_index:
            # new_word をベースに、goal_word の成分を少しだけ（例：20%）混ぜてベクトルをゴールに向ける
            # ※ ここの 0.2 という数値をいじることで、ヒントの「露骨さ（難易度）」を調整できます
            v_hint_direction = 0.8 * self.model[new_word] + 0.2 * self.model[req.goal_word]
            
            # 候補を少し多めに取得
            raw_hints = self.model.similar_by_vector(v_hint_direction, topn=100)
            
            # 出てはいけないNGワード（答えのモロバレや、入力したばかりの言葉）を除外
            forbidden_words = {req.current_word, req.input_word, new_word, req.goal_word}
            
            for w, sim in raw_hints:
                if w not in forbidden_words:
                    hint_words.append(w)
                    # ヒントが5個貯まったら終了
                    if len(hint_words) >= 6:
                        break

        description = self.get_wikipedia_summary(new_word)

        return {
            "new_word": new_word,
            "rank": rank,
            "hint_words": hint_words,
            "description": description
        }

        return CalcResponse(
            new_word=new_word,
            rank=rank,
            hint_words=hint_words,
            description=description
        )