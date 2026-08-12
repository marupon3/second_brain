---
title: Nginx + Flask 本番環境構成（koneta）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2026-02-17 _nginx設定.md
---

# Nginx + Flask 本番環境構成（koneta）

IIS方式（[[Flask本番運用ガイド(Windows・IIS・Waitress)]]）に代わり、後にNginxを使う構成へ移行した際のメモ（`koneta`プロジェクト）。

## 導入手順

1. [Nginx for Windows](https://nginx.org/en/download.html)をダウンロードし`nginx/`ディレクトリに配置
2. `generate_cert.ps1`でSSL証明書を生成
3. Flask起動 → Nginx起動 → `https://localhost/KONETA/auth/login`でアクセス確認

## 証明書の生成（自己署名）

```powershell
cd C:\Users\marupon\PycharmProjects\koneta\nginx
powershell -ExecutionPolicy Bypass -File .\generate_cert.ps1
```

生成される証明書情報の例: Subject Alternative Nameに`localhost`・サーバー名・ローカルIPを含む、有効期間1年。自己署名証明書のため初回アクセス時にブラウザ警告が出るが、社内利用ならクライアントPCの「信頼されたルート証明機関」にインポートすることで警告を回避できる。

## 最終構成

```
Client → HTTPS(8443) → Nginx → HTTP(127.0.0.1:5000) → Flask
```

Nginxはポート80→8080、443→8443にマッピング（ポート番号は`.flaskenv`の`NGINX_HTTPS_PORT`から取得）。

| 項目 | 状態 |
| --- | --- |
| HTTPS通信 | TLS 1.2/1.3 |
| セキュリティヘッダー | X-Frame-Options, HSTS等 |
| Cookie Secure | 有効 |
| ProxyFix | クライアントIPを正常転送 |
| HTTP→HTTPSリダイレクト | 8080→8443 |

## 運用コマンド

| 操作 | コマンド |
| --- | --- |
| Nginx起動 | `koneta\nginx\start_nginx.bat`（管理者権限で実行） |
| Nginx停止 | `koneta\nginx\stop_nginx.bat` |
| Nginx設定リロード | `koneta\nginx\reload_nginx.bat` |
| 証明書更新（期限前） | `generate_cert.ps1` → `reload_nginx.bat` |

## 関連

- [[Flask本番運用ガイド(Windows・IIS・Waitress)|Flask本番運用ガイド（Windows・IIS・Waitress）]]
- [[env暗号化システム運用|.env暗号化システムの運用（webapp5/koneta）]]
