---
created: 2024-02-20
tags: PSQL
---

# PostgreSQL設定

■PostgreSQL　ダウンロードサイト
<https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>
Version 16.2を使用
User:
postgres
PW: !QAZ****
Windows環境変数でPATHを設定　C:\Program Files\PostgreSQL\16\bin
ポスグレウェブ（分かりやすい説明）
<https://postgresweb.com/>
■PostgreSQL を
Windows にインストールするには
<https://qiita.com/tom-sato/items/037b8f8cb4b326710f71>
■pgAdmin4のダウンロード（PostgreSQLのGUIツール）
Version 8.3を使用
<https://www.pgadmin.org/download/pgadmin-4-windows/>
マスターパスワード再設定(2024/9/28)
!QAZ****
pgAdmin 4の使い方(起動からデータ参照)
<https://itsakura.com/pgadmin4-db-create#s2>
テーブルの作成
<https://db-study.com/archives/180>
■PostgreSQL
ODBCドライバーのダウンロード
<https://www.postgresql.org/ftp/odbc/releases/>
psqlodbc_16_00_0000-x64.zip
psqlodbc_16_00_0000-x32.zip（会社用は32bit版）
設定の説明
<https://syutaku.blog/postgresql-install-odbc/>
ODBCデータソース(64ビット)で設定
コントロール パネル\システムとセキュリティ\Windows ツール\ODBCデータソース(64ビット)
![](file3210.files/image001.png)
|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  | <<PostgreSQL.xlsm>> |
|  |  |  |
'VBAの例
Sub ConnectPostgreSQL()
' 接続文字列の設定
Dim conn As ADODB.Connection
Dim rs As ADODB.Recordset
Dim connectionString As String
' PostgreSQLのODBCドライバー名と接続情報を指定(会社用は32bit版）
connectionString = "Driver=PostgreSQL Unicode(X64);" & _
'「ODBCデータソース」の「ドライバー」タブから
"Server=127.0.0.1;" & _
"Port=5432;"
& _
"Database=testDB;" &
_　　’pgAdminを使って自分で設定したデータベース
"Uid=postgres;" & _
"Pwd=!QAZ****;"　　　’PostgreSQLインストール時に自分で設定したPW
Set conn = New ADODB.Connection
Set rs = New ADODB.Recordset
' データベース接続
conn.Open connectionString
' SQLクエリの実行
Set rs = conn.Execute("SELECT * FROM
""Tresource""
LIMIT 10;")　　’’pgAdminで設定したテーブル
' 結果をシート1に貼り付け
Sheet1.Range("A1").CopyFromRecordset rs
' 接続のクローズ
rs.Close
conn.Close
' オブジェクトの解放
Set rs = Nothing
Set conn = Nothing
End Sub
![](file3210.files/image003.png)
psqlODBC(64bit)　v13ドライバ
psqlSQL(64bit)  v16.2-1
pgAgent(64bit)  v4.2.2  インストールせず(v4.8を別途インストール）
