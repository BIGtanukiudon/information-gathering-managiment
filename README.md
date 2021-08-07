# 情報収集管理アプリケーション

スクレイピングを用い、情報を収集するためのアプリケーション。

## 使い方

### サインアップ

`/api/auth/register`でアカウントを登録する。

### 収集先情報登録

`/api/collection_destination/register/`でスクレイピングするための収集先の情報を登録する。

収集したい記事部分の HTML が以下のようになっているとする。

```html
<div class="content">
  <h2 class="entry-title">
    <a href="https://example.com/blog/1" class="content-url">
      コンテンツタイトル
    </a>
  </h2>
  <div>
    <span class="published">2021/08/06</span>
  </div>
  <p>テストコンテンツです。</p>
</div>
```

この場合のリクエストパラメータは以下。

| パラメータ                 | 値の例                | 内容                                                                                                                                                                                       |
| :------------------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | `収集先例`            | 収集先の名前。                                                                                                                                                                             |
| `domain`                   | `https://example.com` | 収集先のドメイン。                                                                                                                                                                         |
| `contents_attr_name`       | `.content`            | 記事部分だと判断できる class 属性のクラス名等。（例：.entry-content。ドットまで入れる。）                                                                                                  |
| `title_attr_name`          | `.entry-title`        | 記事タイトル部分だと判断できる class 属性のクラス名や name 属性の値等。（例：.title。ドットまで入れる。）                                                                                  |
| `published_date_attr_name` | `.published`          | 公開日部分だと判断できる class 属性のクラス名や name 属性の値等。（例：.published-at。ドットまで入れる。）                                                                                 |
| `content_url_attr_name`    | `.content-url`        | 記事本文へ遷移する URL 部分だと判断できる class 属性のクラス名や name 属性の値等。（例：.content-url。ドットまで入れる。）<br>空の場合は`.contet`内に`a`タグがある場合はその値を取得する。 |

### スクレイピングによる記事情報の登録

`/api/content/scraping_contents/`で登録してある収集先情報をもとにスクレイピングを行い、取得した記事情報を登録する。

# インタラクティブ API ドキュメント

`/docs`で Swagger UI によるインタラクティブ API ドキュメントが表示される。

# 本番環境

1. `app/config`下に`.env`ファイルを作成する。`.env`ファイルは`.env.template`をコピーする。
2. イメージをビルドする。
3. `docker-compose.prod.yaml`の`command: pipenv run start`をコメントアウトし、コンテナを起動する。
4. アプリケーションコンテナに入り、DB のマイグレーションを実行する。
5. 一度、関連コンテナを停止し、 `docker-compose.prod.yaml`の`command: pipenv run start`のコメントアウトを外し、再度起動。

## イメージビルド

```cmd
docker-compose -f docker-compose.prod.yaml build
docker-compose -f docker-compose.prod.yaml up -d
```

# 開発環境

# 手順

1. `app/config`下に`.env`ファイルを作成する。`.env`ファイルは`.env.template`をコピーする。
2. イメージをビルドし、アプリケーションを起動する。
3. アプリケーションコンテナに入り、DB のマイグレーションを実行する。
4. `app`ディレクトリ下で`pipenv run start`でを実行し、サーバー起動。

## イメージビルド

```cmd
docker-compose -f docker-compose.dev.yaml build
docker-compose -f docker-compose.dev.yaml up -d
```

## 環境変数

### VS Code Remote Container で開発を行う場合

環境変数`PYTHONPATH`にモジュールパスを追加する。
VS Code Remote Container で開発を行っている場合は以下の環境変数を追加する。

```bash
export PYTHONPATH=/workspace/app/
```

パスが設定されているか以下のスクリプトファイルを実行し、確認。

```py
import sys

for path in sys.path:
    print(path)
```

## Git コミットメッセージのプレフィックス

[AngularJS](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#type)のプレフィックスルールを参考。

- `feat`: 新機能。
- `fix`: バグ修正。
- `docs`: ドキュメントの変更。
- `style`: コードの意味に影響を与えない変更（空白、書式設定、セミコロンの欠落など）。
- `refactor`: バグを修正せず、機能を追加しないコード変更。
- `perf`: パフォーマンスを向上させるコード変更。
- `test`: 不足しているテストを追加する。もしくは、既存のテストを修正する。
- `chore`: ビルドプロセスまたは補助ツールやドキュメント生成などのライブラリへの変更。

# マイグレーション

テーブルを作成するためにアプリケーション側のコンテナ内に入り、マイグレーションを実行する。

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

# env ファイル

`.env`ファイルに環境変数を設定する。

```.env
SECRET_KEY=hoge PWのハッシュ化等に使う
POSTGRES_USER=hoge
POSTGRES_PASSWORD=hoge
POSTGRES_SERVER=hoge
POSTGRES_PORT=5432
POSTGRES_DB=hoge
```

# 注意事項

本作が原因で何らかの損害や障害等が発生したとしても、制作者は一切責任を負わないものとします。
