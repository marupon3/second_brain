---
created: 2024-09-28
tags: PSQL
---

# PostgreSQL設定

(Ver17)
![■PostgreSQL　ダウンロードサイト
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
■PostgreSQL を Windows にインストールするには
https://qiita.com/tom-sato/items/037b8f8cb4b326710f71
無題の画像.png 自動生成された代替テキスト:
Selectthecomponentsyoua猷install:C計thecomponentsyoudonota猷installClickNext
youarereadyto
・postgreSQLServer
ロpgAdmin4
・Stack3uilder
・CommandLineT005
PostgreSQl_databaseserver
無題の画像.png 自動生成された代替テキスト:
PleaseselectadirectoryundernhichStoreyourd
DataDirectory*ProgramFiles*PostgreSQL*17*data
無題の画像.png 自動生成された代替テキスト:
Pleaseprovideapassnordforthedatabasesuperuser(postgresi
Retypepassnord・・・・・・・・|
無題の画像.png 自動生成された代替テキスト:
PleaseselecttheportnumbertheserverShouldlisten
Port5432|
無題の画像.png 自動生成された代替テキスト:
Selectthelocalebeusedbythenendatabasecluster
[Defaultlocale]
Locale
Version 17.01を使用
マスターパスワード: !QAZ****
User: postgres
PW: !QAZ****
Windows環境変数でPATHを設定　C:\Program Files\PostgreSQL\17\bin
ポスグレウェブ（分かりやすい説明）
https://postgresweb.com/
■pgAdmin4-8.12のダウンロード（PostgreSQLのGUIツール）
https://www.pgadmin.org/download/pgadmin-4-windows/
](file4857.files/image001.png)
![https://www.pgadmin.org/download/pgadmin-4-windows/
pgAdmin 4の使い方(起動からデータ参照)
https://itsakura.com/pgadmin4-db-create#s2
テーブルの作成
https://db-study.com/archives/180
■PostgreSQL ODBCドライバーのダウンロード
https://www.postgresql.org/ftp/odbc/releases/
Top → odbc → releases → REL-17_00_0000
psqlodbc_x64.msi
【PostgreSQL】ODBCドライバのインストール手順
https://syutaku.blog/postgresql-install-odbc/
無題の画像.png 自動生成された代替テキスト:
をODBCデ-タソ-スアドミこストレ-タ-国乙ト)
ユ-サーDSNシステムDSNファイルDSNドライバー
システムデ-タソ-スに):
名前プラットフォ-ムドライバ-
トレ-ス
接続プ-ル
バ-ジョン宿報
X
追加(D)…
刳際(R)
程成0…
OD託システムデ-タソ-スには宿定されたデ-タブロバイタ-への接続方法にきす0宿報が納されています。システムデ
づソ-スは、NTサービスを含むこの]ンどュ-ター上のすべてのユ-サ-が認す0ことができます。
キャンセル
(A)
ヘルプ
無題の画像.png 自動生成された代替テキスト:
デタソ-スの新規作成
セ針、アップするテ-タソ-スの汚イバ-を選択してください(S)
MにrosoftExcelDnver(*.xls′
PostgreSQLANSI
PostgreSQLANSI(x64)
X
.xx..
PostgreSQLODBCDnver(UNICODE)
PostgreSQLOD託Driver(ANSI)
PostgreSQLlJnにOde
SQLServer
PostgreSQLunにOdX6
(民引町
完了
バ-ジョン
15.00.17928.
17.00.00.00
17.00.00.00
13.02.00.00
13.02.00.00
17.00.00.00
17.00.00.00
1圧00.25100.
キャンセル
](file4857.files/image002.png)
![無題の画像.png 自動生成された代替テキスト:
デタソ-スの新規作成
セ針、アップするテ-タソ-スの汚イバ-を選択してください(S)
MにrosoftExcelDnver(*.xls′
PostgreSQLANSI
PostgreSQLANSI(x64)
X
.xx..
PostgreSQLODBCDnver(UNICODE)
PostgreSQLOD託Driver(ANSI)
PostgreSQLlJnにOde
SQLServer
PostgreSQLunにOdX6
(民引町
完了
バ-ジョン
15.00.17928.
17.00.00.00
17.00.00.00
13.02.00.00
13.02.00.00
17.00.00.00
17.00.00.00
1圧00.25100.
キャンセル
ODBCデータソース(64ビット)で設定
コントロール パネル\システムとセキュリティ\Windows ツール\ODBCデータソース(64ビット)
無題の画像.png 自動生成された代替テキスト:
p。5t9「eSQLUnicodeODBCセットアップ
テ-タソ-ス名:
日月:(D)
SSLMode:(L)
サ-パ-名:
テ-タベ-ス名:
既定の
ユ-ザ-名:
パスワ-ド:
無効
127』』.1
maruponDB
PostgreSQL85W
postgres
X
テスト
保存
キャンセル
Port:
5432
オプシコン(髙度な定)
テ-タソ-ス
全体定
PostgreSQLVer7.3Copyright(C)18-2圓8;
InsightDistributionSystems
Intheoriginalform,JapanesepatchHiroshトSaito
無題の画像.png 自動生成された代替テキスト:
を
ODBCデ
ユ-サ-DSN
このコンヒュ-タ-にインスト-ルされているOD託ライバ-(0):
システムDSNファイルDSNドライバ-トレ-ス
-タソ-スアドミこストレ-タ国乙ト)
PostgreSQLunにode(x64':
SQLServer
PostgreSQLlJnにOde
PostgreSQLODBCDnver(UNICODE)
PostgreSQLOD託Driver(ANSI)
PostgreSQLANSI(x64)
PostgreSQLANSI
Mにro代cDriver(をxls,をxx′をxm′*.xlsb)
MにrosoftAccessTextDriver(*.txt*.csv)
接続プ-ル
バ-ジョン宿報
X
15.00.17928.20018
15.00.17928.20018
17.00.00.00
17.00.00.00
13.02.00.00
13.02.00.00
17.00.00.00
17.00.00.00
10.00.25100.1455
MにrosoftCorporation
MにrosoftCorporation
PostgreSQLGlobal
PostgreSQLGlobal
PostgreSQLGlobal
PostgreSQLGlobal
PostgreSQLGlobal
PostgreSQLGlobal
M•crosoftCorporation
OD託汚イバ-を用すると、OD託が有効なプログラムでOD託テ-タソスガら信報を取得することカ第きます。
新しい汚イバ-をインスト-ルす引こは、ライバ-のセ針、アッププログラムを用してください。
キャンセル
(A)
ヘルプ
設定終了
無題の画像.png 自動生成された代替テキスト:
pg,Adm-n
ファイルオプジェクトッ-ルEditViewWindowヘルプ
オプシェクトェクスプロ-ラ
、・目servers(1)
、・ダpostgreSQL17
〉・ロクイン/クル-プロ
〉芒テ-プル空問
postgres
maruponOB
-タへ-ス(2)
-丿レ
](file4857.files/image003.png)
![テスト用のデータベース作成
無題の画像.png 自動生成された代替テキスト:
圉作成-テ-プル
-般列
名前
所有者
スキーマ
詳細設定
制約
八-ティション
world
Apostgres
•public
ご]pg_default
八ラメ-タ
セキュリティ
SQL
丁ーフル空間
ィまノヨ)′つ---
フル
X閉しる
つリセット
X
日保存
無題の画像.png 自動生成された代替テキスト:
作成-テ-プル
-般列
継承兀テープル
詳細設定
country
capital
制約
八-ティション
|継承元を取得~
デ-タ型
八ラメ-タ
セキュリティ
列
長さ/精度
SQL
スケ-ル
charactervarying
charactervarying
NOTNULL
X閉しる
つリセット
X
十
a保存
'VBAの例Sub ConnectPostgreSQL()
' 接続文字列の設定
Dim conn As ADODB.Connection
Dim rs As ADODB.Recordset
Dim connectionString As String
' PostgreSQLのODBCドライバー名と接続情報を指定
無題の画像.png 自動生成された代替テキスト:
pg,Adm-n
ファイルオプジェクトッ-ルEditViewWindowヘルプ
オプシェクトェクスプロ-ラ
、・目servers(1)
、・ダpostgreSQL17
〉・ロクイン/クル-プロ
〉芒テ-プル空問
、・当丁-タへ-ス(2)
、・とゴmaruponOB
>二イベントトリカ
>彎カタログ
>キャスト
-丿レ
>サプスクリプション
、・曾スキーマ(1)
、・・public
〉1--3シ-ケンス
、・テ-プル(1)
〉巴world
](file4857.files/image004.png)
![    ' PostgreSQLのODBCドライバー名と接続情報を指定
connectionString = "Driver=PostgreSQL Unicode(X64);" & _  '「ODBCデータソース」の「ドライバー」タブから
"Server=127.0.0.1;" & _
"Port=5432;" & _
"Database=maruponDB;" & _　　’pgAdminを使って自分で設定したデータベース
"Uid=postgres;" & _
"Pwd=!QAZ****;"　　　’PostgreSQLインストール時に自分で設定したPW
Set conn = New ADODB.Connection
Set rs = New ADODB.Recordset
' データベース接続
conn.Open connectionString
' SQLクエリの実行
Set rs = conn.Execute("SELECT * FROM world LIMIT 10;")　　’’pgAdminで設定したテーブル
' 結果をシート1に貼り付け
Sheet1.Range("A2").CopyFromRecordset rs
' 接続のクローズ
rs.Close
conn.Close
' オブジェクトの解放
Set rs = Nothing
Set conn = Nothing
End Sub
](file4857.files/image005.png)
![](file4857.files/image006.png)
psqlODBC(64bit)　v13ドライバ
psqlSQL(64bit)  v16.2-1
pgAgent(64bit)  v4.2.2  インストールせず(v4.8を別途インストール）
