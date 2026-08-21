---
created: 2025-01-04
tags: PSQL
---

# PostgreSQLバージョンアップ

Ver. 17.0.1 →　Ver.
17.2.3 (2025/1/4)　→　 Ver. 17.3 (2025/2/16)
1. バックアップを取得する
pg_dumpallコマンドを使用してすべてのデータベースをバックアップする。（コマンドプロンプト）
psql --version
$env:PGPASSWORD = "postgres"　（パスワードを設定）
pg_dumpall -U postgres -f C:\Users\marupon\Desktop\full_backup.sql
1. PostgreSQL公式サイトから新バージョンをダウンロード
（
<https://www.postgresql.org/download/windows/）にアクセスします>
1. 現行バージョンを停止
コマンドプロンプトを管理者権限で開いて、以下のコマンドを入力。
net stop postgresql-x64-17
1. 新しいバージョンのインストール
1. ダウンロードしたインストーラーを起動します。
2. インストール中の選択肢で、以下の点を確認してください:
* 同じデータディレクトリを使用するか、新しいディレクトリを指定するかを選べます。
（通常、既存のデータディレクトリを使用することが推奨されますが、事前のバックアップが必須です。）
* "Upgrade an
existing PostgreSQL installation"オプションが表示される場合は、それを選択します。
5. 設定の確認
インストールが完了したら、設定ファイル（postgresql.confやpg_hba.conf）を確認し、必要に応じて以前の設定を反映します。
（C:\Program
Files\PostgreSQL\17\data）
6. サービスの再起動と動作確認
1. PostgreSQLサービスを再起動します:
sql
コードをコピーする
net start postgresql-x64-17
1. psqlなどを使用して、データベースが正常に動作しているか確認します。
7. アップデート後のテスト
バックアップからリストアが必要ないことを確認するために、いくつかのクエリを実行してデータの整合性をチェックしてください。
psql -U postgres
パスワードを再設定する場合 $env:PGPASSWORD = "your_password"
【SQL】
ALTER USER maruponDB PASSWORD 'new_password';
ALTER USER postgres PASSWORD 'new_password';
問題の可能性と解決方法
1. パスワードが不明または間違っている
postgres または
marupon ユーザーのパスワードが正しく設定されていない可能性があります。
対応方法:
1. postgres
ユーザーのパスワードをリセットします。
powershell
コードをコピーする
psql -U postgres
（scram-sha-256 の認証にパスワードが必要ですが、これが失敗する場合は次のセクションを参照してください。）
2. パスワードをリセットする SQL
コマンドを実行します。
sql
コードをコピーする
postgres=#　ALTER USER postgres PASSWORD
'new_password';
postgres=#　ALTER USER marupon PASSWORD 'new_password';
2. 一時的に認証方法を緩和する
認証方式を一時的に trust
に変更してパスワード認証を不要にします。これにより、接続トラブルを解消し、必要な修正を行えます。
修正手順:
1. pg_hba.conf
を編集し、認証方式を trust に変更します。
plaintext
コードをコピーする
# TYPE  DATABASE        USER            ADDRESS                 METHOD
#
"local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
1. PostgreSQL
サーバーを再起動します。
* Windows:
powershell
コードをコピーする
net stop postgresql-x64-17
net start postgresql-x64-17
2. パスワードなしで接続が可能になります。この状態で必要なパスワードリセットを行います。
powershell
コードをコピーする
psql -U postgres
postgres=#　ALTER USER postgres PASSWORD 'new_password';
postgres=#　ALTER USER marupon PASSWORD
'new_password';
1. パスワードをリセット後、pg_hba.conf
を元の scram-sha-256 に戻し、再度サーバーを再起動します。
3. IPv6 アドレスの影響
エラーメッセージに
"::1"（IPv6 のローカルループバックアドレス）が含まれている場合、IPv6 接続に問題がある可能性があります。
対応方法:
* IPv4 を優先して接続を試みます。
powershell
コードをコピーする
psql -U postgres -h 127.0.0.1
4. PostgreSQL サーバーが起動しているか確認
サーバーが正しく起動していない場合、認証以前の問題で接続が失敗します。
確認手順:
* サーバーが実行中であることを確認します。
powershell
コードをコピーする
net start | findstr PostgreSQL
* 実行していない場合、以下のコマンドで起動します。
powershell
コードをコピーする
net start postgresql-x64-17
5. 変更後のテスト
以上の手順を実行後、接続テストを行います。
テストコマンド:
powershell
コードをコピーする
psql
-U postgres -h localhost
* 正常に接続できる場合、設定は問題ありません。
* 接続に失敗する場合、エラー内容を再確認してください。
