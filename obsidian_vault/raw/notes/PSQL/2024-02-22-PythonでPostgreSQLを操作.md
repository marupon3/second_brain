---
created: 2024-02-22
tags: PSQL
---

# PythonでPostgreSQLを操作

[PythonでPostgreSQLを操作する（psycopg2）
(python-work.com)](https://python-work.com/postgresql-psycopg2/)
使用ライブラリ
ライブラリのインストール
PostgreSQLを準備する
PostgreSQLのインストール（Windows）
データベースを作成する
テーブルを作成する
ライブラリのインポート
レコードを挿入する（INSERT）
複数レコードを一括で挿入する（INSERT）
データを取得する（SELECT）
データを1件ずつ取得する
全データを取得する
辞書型で取得する
データフレームに変換
列名を取得してデータフレームの列名に反映する
データの更新（UPDATE）
データの削除（DELETE）
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  | <<PostgreSQ_pythonL.zip>> |  | <<postges_data.csv>> |
#　PostgreSQLからデータを取得
#　PostgreSQLからデータを取得（データフレーム）

<!-- 変換時の注記: OneNote由来の改行を括弧深さ/構文解析で自動復元しました。インデントはOneNote側で失われている場合があり保証されません。実行前に必ず目視確認してください（要確認）。 -->

```python
import psycopg2
import pandas as pd
# PW関連モジュール
from dotenv import load_dotenv
import os
# 環境変数をロードする
load_dotenv()
#
環境変数からデータベース接続情報を取得する
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
# データベースに接続
connection = psycopg2.connect(host='localhost', user= db_user, password= db_password, database='testDB')
"""データフレーム型で取得する(列名入り） """ with connection: with connection.cursor() as cursor: # データ読み込み sql = "SELECT * FROM \"Tresource\" LIMIT 20;" cursor.execute(sql) cols = [col.name for col in cursor.description] df = pd.DataFrame(cursor.fetchall(),columns = cols) print(df) # コネクションのクローズ connection.close()
```
