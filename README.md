# イメージビルド

```cmd
docker-compose -f docker-compose.dev.yaml build
docker-compose -f docker-compose.dev.yaml up -d
```

# 開発環境

## 環境変数

環境変数`PYTHONPATH`にモジュールパスを追加する。
VS Code Remote Containerで開発を行っている場合は以下の環境変数を追加する。

```bash
export PYTHONPATH=/workspace/app/database/:/workspace/app/
```

パスが設定されているか以下のスクリプトファイルを実行し、確認。

```py
import sys

for path in sys.path:
    print(path)
```

# マイグレーション

## マイグレーションファイル作成

```bash
cd app
alembic revision -m "hogehoge"
```

## 実行

```bash
cd app
alembic upgrade head
```