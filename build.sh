#!/usr/bin/env bash

# 環境変数の読み込み（必要であれば .env が存在する場合）
if [ -f .env ]; then
  echo "🔄 .env 読み込み中"
  export $(grep -v '^#' .env | xargs)
fi

# マイグレーション実行
echo "📦 データベースマイグレーション"
python manage.py migrate --noinput

# 静的ファイル収集
echo "🗂️ staticfiles を収集"
python manage.py collectstatic --noinput

echo "✅ build.sh 実行完了"
