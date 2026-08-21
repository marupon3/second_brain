---
created: 2024-06-07
tags: python
---

# Apache+FastAPI

Apach2.4
download
<https://www.apachelounge.com/download/>
PythonのFastAPIフレームワークを使ったWEBアプリケーション
WEBアプリをサーバーに載せクライアントPCから利用
【環境】
サーバー環境;Windows11
64bit版
Python 3.7.8
Pythonは仮想環境(venv)で使用
HTTPサーバー:Apache2.4
【Path】
FastAPIの親ディレクトリ: C:\Users\marupon\PycharmProjects\FastAPI_test
実行ファイル: C:\Users\marupon\PycharmProjects\FastAPI_test\main.py
Appache: C:\Apchte24\bin　（環境変数にPathを通す）
Python本体: C:\Users\marupon\AppData\Local\Programs\Python\Python37\python.exe
【Apacheのインストール】
httpd.exe -k
install
【操作】
C:\Apache24\conf\httpd.conf ファイルを修正する
LoadModule
proxy_module modules/mod_proxy.so
LoadModule
proxy_http_module modules/mod_proxy_http.so
<VirtualHost
*:80>
ServerName 192.168.10.110　#http://は不要、項目が元からある場合はコメントアウト
ProxyPass
/ <http://192.168.10.110:8000/>
ProxyPassReverse
/ <http://192.168.10.110:8000/>
</VirtualHost>
Apacheを再起動する
C:\>
C:\Apache24\bin\httpd.exe -k restart
(停止は、http.exe -k stop)
仮想環境をアクティベートする
cd
C:\Users\marupon\PycharmProjects\FastAPI_test
venv\Scripts\activate
main.pyを実行する
uvicorn
main:app --host 0.0.0.0 --port 8000 --reload
ローカルPCからアクセスして確認する
<http://192.168.10.110/fastapi-test>
PC起動時にmain.pyを実行するバッチファイルを作成
（fastapi-test.bat)
@echo
off
cd
C:\Users\marupon\PycharmProjects\FastAPI_test
call
venv\Scripts\activate.bat
uvicorn
main:app --host 0.0.0.0 --port 8000 --reload
バッチファイルをタスクスケジューラに登録する
【テスト用:main.py】

<!-- 変換時の注記: OneNote由来の改行を括弧深さ/構文解析で自動復元しました。インデントはOneNote側で失われている場合があり保証されません。実行前に必ず目視確認してください（要確認）。 -->

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/fastapi-test") def read_root():
    return {"Hello": "World!"}
ポート8000を使用しているプロセスの詳細を取得
netstat -ano | findstr :8000 PIDに関連するプロセスの詳細を取得（プロセス番号が1234の例） tasklist /fi "PID eq 1234" プロセスを切る taskkill /F /pid <kill したい PID> Apacheを再起動する C:\> C:\Apache24\bin\httpd.exe -k restart
```
