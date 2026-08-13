---
title: Webサーバー運用メモ（IIS・Apache・FastAPI）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2024-05-28 IISマネージャーに関するコマンド.md
  - obsidian_vault/raw/notes/Python/2024-06-04 Apacheインストールと設定.md
  - obsidian_vault/raw/notes/Python/2024-06-07 Apache+FastAPI.md
---

# Webサーバー運用メモ（IIS・Apache・FastAPI）

## IISマネージャー関連コマンド

```
# IISマネージャーを開く（Windowsボタン+R）
inetmgr

# IISサービス停止/開始
iisreset /stop
iisreset /start

# ポート8000を使用しているプロセスを特定
netstat -ano | findstr :8000
tasklist /fi "PID eq 1234"
```

## Apacheのインストールと設定（Windows）

1. [Apache Lounge](https://www.apachelounge.com/download/)からApache Win64bitとVC_redist（Visual C++ライブラリ）をダウンロード
2. `cd C:\Apache24\bin` → `httpd.exe -k install`
3. `C:\Apache24\conf\httpd.conf`の`ServerName`行のコメント`#`を外して保存
4. `ApacheMonitor.exe`でStart/Stop/Restart操作（タスクバーに常駐アイコン）
5. IISが起動中だとポート80が競合するため停止: `net stop WAS`（開始は`net start WAS`）
6. `http://localhost/`でApacheの起動確認

このケースでは最終的にApacheは不採用とし、IISとWaitressで運用することにした。

## Apache + FastAPI（リバースプロキシ構成）

Windows 11 + Python 3.7.8（venv）+ FastAPI + Apache 2.4のリバースプロキシ構成でWebアプリをサーバー上に公開する手順。

### httpd.confの設定

```
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so

<VirtualHost *:80>
    ServerName 192.168.10.110
    ProxyPass / http://192.168.10.110:8000/
    ProxyPassReverse / http://192.168.10.110:8000/
</VirtualHost>
```

設定後は`httpd.exe -k restart`で再起動（停止は`-k stop`）。

### FastAPIアプリの起動

```
cd C:\Users\marupon\PycharmProjects\FastAPI_test
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

テスト用`main.py`:

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/fastapi-test")
def read_root():
    return {"Hello": "World!"}
```

### PC起動時に自動実行するバッチファイル（タスクスケジューラ登録）

```bat
@echo off
cd C:\Users\marupon\PycharmProjects\FastAPI_test
call venv\Scripts\activate.bat
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### プロセスのトラブルシューティング

```
netstat -ano | findstr :8000
tasklist /fi "PID eq 1234"
taskkill /F /pid <killしたいPID>
```

## 関連

- [[postgresql|PostgreSQL運用メモ]]
- [[Python開発環境構築]]
