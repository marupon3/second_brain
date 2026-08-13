---
メモ: 2025-04-12
source: OneNote
作成時刻: 9:31
---

# _PostgreSQLのパスワードリセット方法

Gensparkのディープリサーチで出力
PostgreSQLのパスワードがわからなくなった場合、主に以下の方法でリセットすることができます。
pg_hba.confファイルを編集してパスワード認証をスキップする
手順:
Windows管理ツールの「サービス」を開く
「postgresql-x64-16」のようなサービスを見つけ、右クリックして「停止」を選択
1. pg_hba.confファイルを探す
Windows: 通常は C:\Program
Files\PostgreSQL\16\data\pg_hba.conf
1. pg_hba.confファイルを編集
ファイルを管理者権限で開きます
以下のような行を探します:
# IPv4 local connections:
host
all             all             127.0.0.1/32            md5
# IPv6 local connections:
host
all             all             ::1/128                 md5
md5 または scram-sha-256 となっている箇所を trust
に変更します
# IPv4 local connections:
host
all             all             127.0.0.1/32            trust
# IPv6 local connections:
host
all             all             ::1/128                 trust
また、local 行も同様に変更します:
local
all             all                                     trust
1. PostgreSQLサービスを再起動
Windows: サービスマネージャーからPostgreSQLサービスを再起動
1. パスワードなしでPostgreSQLに接続
psql -U postgres
この時点でパスワードを要求されずに接続できるはずです
1. 新しいパスワードを設定
以下のSQLコマンドを実行してパスワードを変更します:
ALTER ROLE
postgres WITH PASSWORD '新しいパスワード';
1. pg_hba.confを元に戻す
手順2で変更した設定を元に戻します（trustをmd5やscram-sha-256に戻す）
1. PostgreSQLサービスを再起動
手順3と同じコマンドでサービスを再起動します
