---
title: PostgreSQL運用メモ
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/PSQL/2024-02-20 PostgreSQLバージョンアップ.md
  - obsidian_vault/raw/notes/PSQL/2024-02-20 PostgreSQL設定.md
  - obsidian_vault/raw/notes/PSQL/2024-02-22 240222 PythonでPostgreSQLを操作.md
  - obsidian_vault/raw/notes/PSQL/2024-02-24 Postgres 0埋め.md
  - obsidian_vault/raw/notes/PSQL/2024-02-29 KNIMEとの連携, JDBC.md
  - obsidian_vault/raw/notes/PSQL/2024-02-29 PostgreSQL説明書.md
  - obsidian_vault/raw/notes/PSQL/2024-03-02 PostgreSQLのエクスポートとインポート.md
  - obsidian_vault/raw/notes/PSQL/2024-04-19 tableの結合.md
  - obsidian_vault/raw/notes/PSQL/2024-06-14 テーブルの一括登録.md
  - obsidian_vault/raw/notes/PSQL/2024-06-14 数値データ型.md
  - obsidian_vault/raw/notes/PSQL/2024-09-19 医薬品検索にベクトル検索を導入したら、デフォで検索ニーズをほぼ満たせそうだった話.md
  - obsidian_vault/raw/notes/PSQL/2024-09-28 PostgreSQL設定.md
  - obsidian_vault/raw/notes/PSQL/2024-11-10 SQLの書き方.md
  - obsidian_vault/raw/notes/PSQL/2025-01-03 データベース削除.md
  - obsidian_vault/raw/notes/PSQL/2025-01-04 _PostgreSQLバージョンアップ.md
  - obsidian_vault/raw/notes/PSQL/2025-01-04 _データベース名取得.md
  - obsidian_vault/raw/notes/PSQL/2025-04-12 250411_データベースバックアップ手順.md
  - obsidian_vault/raw/notes/PSQL/2025-04-12 _PostgreSQLのパスワードリセット方法.md
  - obsidian_vault/raw/notes/PSQL/2025-11-08 _テーブルをPCに出力.md
  - obsidian_vault/raw/notes/PSQL/2025-11-09 _項目をカンマ区切りで出力.md
  - obsidian_vault/raw/notes/PSQL/2026-02-02 _テーブル構成を出力.md
---

# PostgreSQL運用メモ

Windows環境でのPostgreSQL個人運用に関する一連のメモ。パスワード等の秘密情報は原文に含まれていたが、本ページでは伏字にして記載していない。

## インストール・設定

- ダウンロード: <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>
- Windows環境変数PATHに`C:\Program Files\PostgreSQL\<version>\bin`を追加
- pgAdmin4（GUIツール）: <https://www.pgadmin.org/download/pgadmin-4-windows/>
- 参考: [ポスグレウェブ](https://postgresweb.com/)、[Windowsインストール手順](https://qiita.com/tom-sato/items/037b8f8cb4b326710f71)、[pgAdmin4の使い方](https://itsakura.com/pgadmin4-db-create#s2)、[テーブル作成](https://db-study.com/archives/180)
- ODBCドライバー: <https://www.postgresql.org/ftp/odbc/releases/>（64bit版を「ODBCデータソース(64ビット)」で設定。会社用など32bit環境が必要な場合は32bit版を使用）
- 公式マニュアル: <https://pgsql-jp.github.io/jpug-doc/15.4/postgresql-15.4-A4.pdf>、<https://www.postgresql.jp/docs/9.2/index.html>
- 数値データ型: <https://www.postgresql.jp/docs/15/datatype-numeric.html>
- SQLの実務的な書き方（PostgreSQLConf資料）: <https://speakerdeck.com/soudai/pgcon21j-tutorial>

### VBAからの接続例

```vba
Sub ConnectPostgreSQL()
    Dim conn As ADODB.Connection
    Dim rs As ADODB.Recordset
    Dim connectionString As String
    connectionString = "Driver=PostgreSQL Unicode(X64);" & _
        "Server=127.0.0.1;" & _
        "Port=5432;" & _
        "Database=<データベース名>;" & _
        "Uid=postgres;" & _
        "Pwd=<パスワード>;"
    Set conn = New ADODB.Connection
    Set rs = New ADODB.Recordset
    conn.Open connectionString
    Set rs = conn.Execute("SELECT * FROM ""<テーブル名>"" LIMIT 10;")
    Sheet1.Range("A1").CopyFromRecordset rs
    rs.Close
    conn.Close
    Set rs = Nothing
    Set conn = Nothing
End Sub
```

### Python（psycopg2）からの接続例

```python
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

connection = psycopg2.connect(host='localhost', user=db_user, password=db_password, database='testDB')
with connection:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM \"Tresource\" LIMIT 20;"
        cursor.execute(sql)
        cols = [col.name for col in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=cols)
        print(df)
connection.close()
```

参考: <https://python-work.com/postgresql-psycopg2/>

### KNIME（JDBC接続）

PostgreSQL ConnectorノードでJDBCドライバー（`postgresql-42.7.2.jar`）を使用。ダウンロード: <https://jdbc.postgresql.org/download/>

## バージョンアップ手順

1. `pg_dumpall -U postgres -f <backup.sql>`で全データベースをバックアップ
2. 公式サイトから新バージョンをダウンロード
3. `net stop postgresql-x64-<version>`で現行サービスを停止
4. インストーラーで既存データディレクトリを指定し"Upgrade an existing PostgreSQL installation"を選択
5. `postgresql.conf`/`pg_hba.conf`の設定を確認
6. `net start postgresql-x64-<version>`でサービス再起動、動作確認

### トラブルシューティング（認証エラー時）

`pg_hba.conf`の該当行（local/host）を一時的に`trust`に変更 → サービス再起動 → パスワードなしで接続し`ALTER USER <user> PASSWORD '<新パスワード>';`でリセット → 設定を`scram-sha-256`等に戻して再起動。IPv6（`::1`）接続で問題が出る場合は`psql -U postgres -h 127.0.0.1`とIPv4を明示。

## パスワードリセット手順

1. Windowsサービスで該当PostgreSQLサービスを停止
2. `pg_hba.conf`（例: `C:\Program Files\PostgreSQL\16\data\pg_hba.conf`）の認証方式（md5/scram-sha-256）を`trust`に変更
3. サービス再起動 → `psql -U postgres`でパスワードなし接続
4. `ALTER ROLE postgres WITH PASSWORD '<新パスワード>';`
5. `pg_hba.conf`を元に戻してサービス再起動

## バックアップ・リストア

- 論理バックアップ（`pg_dump`/`pg_dumpall`）: バージョン間移行がしやすく、特定テーブルのみの抽出も可能。初心者にはこちらを推奨
- 物理バックアップ: データファイルをそのままコピー。大規模DBで高速だが同一バージョン限定
- GUI（pgAdmin4）: データベースを右クリック→「バックアップ...」、形式は「カスタム」推奨（圧縮率5〜7程度）
- コマンド例: `pg_dump -U postgres -F c -b -v -f "C:\backup\mydb.backup" mydb`
- リストア: `pg_restore -U postgres -d mydb -v "C:\backup\mydb.backup"`（カスタム/tar/ディレクトリ形式）、`psql -U postgres -d mydb -f "C:\backup\mydb.sql"`（テキスト形式）
- 定期バックアップ: バッチファイル（`pg_dump`をタイムスタンプ付きファイル名で実行）を作成し、Windowsタスクスケジューラで定期実行

## データベース操作

### データベース削除

```sql
psql -U postgres -h localhost -d <database>
\c postgres
DROP DATABASE <database>;
```

### データベース一覧・名前取得

```sql
\l
-- または
SELECT datname FROM pg_database;
```

## テーブル操作

### 0埋め

```sql
-- LPAD関数
SELECT LPAD(id::text, 5, '0') FROM your_table;
-- TO_CHAR関数
SELECT TO_CHAR(id, 'FM00000') AS formatted_id FROM your_table WHERE id = 123;
```

### テーブル結合

```sql
-- 内部結合
SELECT カラム名1, カラム名2 FROM テーブル1 INNER JOIN テーブル2 ON 結合条件;
-- 外部結合（例）
SELECT users.id, users.name, orders.order_date, orders.total_amount
FROM users LEFT OUTER JOIN orders ON users.id = orders.user_id;
```

### CSV一括登録（\copy）

```sql
\copy tkcode(depart, stage, task, tkcode) FROM 'C:\\Users\\marupon\\Desktop\\new_data.csv' DELIMITER ',' CSV HEADER;
```

旧バージョンでは`COPY`コマンド（サーバー側ファイル読み込み）を使用。

### テーブルをCSVにエクスポート

```sql
psql -U postgres -d fulltextsearch -c "\copy (SELECT * FROM textdata) TO 'C:/Users/marupon/Downloads/textdata.csv' WITH CSV HEADER"
```

### カラムをカンマ区切りで集約

```sql
SELECT string_agg(original_word, ',' ORDER BY word_id ASC) AS csv_text
FROM (
    SELECT original_word, word_id FROM public.word_dictionary ORDER BY word_id ASC LIMIT 200
) AS t;
```

### テーブル構成（スキーマ情報）の一覧出力

```sql
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('access_logs', 'crawl_schedules', 'document_metadata', 'inverted_index',
                      'search_targets', 'textdata', 'user_dictionary', 'user_search_folders', 'word_dictionary')
ORDER BY table_name, ordinal_position;
```

### エクスポート／インポート（pg_dump/psql）

```
# エクスポート
pg_dump -U postgres -t table01 -f C:\Users\marupon\Desktop\table01_dump.sql testdb
# インポート
psql -U postgres -d tcmg -f C:\Users\marupon\Desktop\table01_dump.sql
```

## 関連

- 全文検索拡張は[[pgroonga|PGroonga]]を参照
- 医薬品検索へのベクトル検索導入事例（外部記事）: <https://zenn.dev/minedia/articles/d9f01aa05bc880>

## 内容未記入・空のためページ化しなかったもの

`SQL 主キー.md`、`TCMG(リソースDX).md`、`SQLチートシート.md`、`2024-10-25 PostgreSQLバージョンアップ.md`、`2025-01-04 SQLチート.md`
