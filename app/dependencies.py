# dependencies.py とは？
#
# FastAPI の「どのエンドポイントでも共通で使いたい処理」を書く場所。
# 今は中身がほぼないが、将来ここに追加する予定のもの：
#   - APIキー認証（リクエストヘッダーにキーが含まれているか確認）
#   - レートリミット（1秒に何回まで呼べるか制限）
#   - ログ出力（すべてのリクエストをロギング）
#
# 今は使わないので、ほぼ空のままでOK。
# FastAPI 公式の構成に倣ってファイルだけ置いておく。

from fastapi import Header


async def verify_token(x_token: str = Header(default=None)):
    """
    将来的なAPIキー認証の雛形。
    今は何もチェックしないが、本番化するときにここを実装する。
    """
    # TODO: 本番化する際にAPIキーの検証ロジックを追加する
    pass
