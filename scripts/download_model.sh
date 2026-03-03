#!/bin/sh
# ============================================================
# download_model.sh — word2vec モデルのダウンロードスクリプト
# ============================================================
# WikiEntVec の学習済みモデルをダウンロード・解凍します。
# モデルファイルが既に存在する場合はスキップします。
# ============================================================
set -eu

MODEL_DIR="/app/app/models"
MODEL_FILE="${MODEL_DIR}/jawiki.word_vectors.200d.txt"
MODEL_URL="https://github.com/singletongue/WikiEntVec/releases/download/20190520/jawiki.word_vectors.200d.txt.bz2"

# 既にモデルが存在する場合はスキップ
if [ -f "${MODEL_FILE}" ]; then
    echo "[model] モデルファイルは既に存在します: ${MODEL_FILE}"
    exit 0
fi

echo "[model] モデルをダウンロード中..."
echo "[model] URL: ${MODEL_URL}"

TEMP_FILE="${MODEL_FILE}.bz2"

# ダウンロード実行
curl -fSL --progress-bar -o "${TEMP_FILE}" "${MODEL_URL}"

# bzip2 解凍
echo "[model] bzip2 ファイルを解凍中..."
bzip2 -d "${TEMP_FILE}"

echo "[model] ダウンロード完了: ${MODEL_FILE}"
ls -lh "${MODEL_FILE}"
