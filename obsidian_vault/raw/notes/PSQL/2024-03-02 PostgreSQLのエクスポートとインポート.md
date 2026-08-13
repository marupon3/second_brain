---
メモ: 2024-03-02
source: OneNote
作成時刻: 22:17
---

# PostgreSQLのエクスポートとインポート

<https://itsakura.com/postgresql-export#s1>
テーブルの出力(ユーザ名、テーブル名、保存場所、データベース名）
【cmd】
pg_dump
-U postgres -t table01 -f C:\Users\marupon\Desktop\table01_dump.sql
testdb
テーブルの入力(ユーザ名、データベース名、保存場所）
【cmd】
psql
-U postgres　-d tcmg
-f C:\Users\marupon\Desktop\table01_dump.sql
