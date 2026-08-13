---
title: Flask本番運用ガイド（Windows・IIS・Waitress）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2025-04-07 _代替WSGIサーバ.md
  - obsidian_vault/raw/notes/Python/2025-04-19 _Windowsファイアウォール設定.md
  - obsidian_vault/raw/notes/Python/2025-04-20 アクセスログ設定.md
  - obsidian_vault/raw/notes/Python/2025-04-20 本番環境に向けての改善.md
  - obsidian_vault/raw/notes/Python/2025-04-21 _IIS導入.md
  - obsidian_vault/raw/notes/Python/2025-04-21 リバースプロキシ設定.md
  - obsidian_vault/raw/notes/Python/2025-04-21 _SSL\TLS証明書を取得.md
  - obsidian_vault/raw/notes/Python/2025-04-30 _LDAP認証のスキップ設定.md
---

# Flask本番運用ガイド（Windows・IIS・Waitress）

個人開発のFlaskアプリ（crud、pulldownlist等）をWindows環境で本番運用するための一連のメモ。

## WSGIサーバー: Waitress

Flask開発サーバーの警告（"Do not use it in a production deployment"）が出た場合、Windows環境ではWaitressを使う。

```
pip install waitress
waitress-serve --port=8000 main:app
waitress-serve --host 127.0.0.1 --port 8000 main:app
```

参考: <https://lazy-developer.jp/flask-wsgi-waitress>

## Windowsファイアウォールでポートを開放する

```powershell
# ポート8000を開放
New-NetFirewallRule -DisplayName "Allow Waitress 8000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000

# ルールの状態確認
Get-NetFirewallRule -Name "AllowWaitress8000" | Format-Table Name, DisplayName, Enabled, Direction, @{N='Port';E={$_.LocalPort}}

# 一時的に無効化/再有効化
Set-NetFirewallRule -DisplayName "Allow Waitress 8000" -Enabled False
Set-NetFirewallRule -DisplayName "Allow Waitress 8000" -Enabled True

# 完全に削除
Remove-NetFirewallRule -DisplayName "Allow Waitress 8000"
```

## IISの導入とリバースプロキシ設定

### Windows Server: サーバーマネージャーから導入

サーバーマネージャー →「管理」→「役割と機能の追加」→ ロールベースのインストール →「Webサーバー(IIS)」を選択。役割サービスは「静的コンテンツ」「HTTPリダイレクト」「Windows認証」「IIS管理コンソール」等を確認。

### Windows 10/11: コントロールパネルから導入

「プログラムと機能」→「Windowsの機能の有効化または無効化」→「インターネットインフォメーションサービス」にチェック。

### 拡張モジュールの追加（リバースプロキシに必須）

- [URL Rewrite Module](https://www.iis.net/downloads/microsoft/url-rewrite)
- [Application Request Routing (ARR)](https://www.iis.net/downloads/microsoft/application-request-routing)

### リバースプロキシ設定（IIS + ARR）

1. IISマネージャーでサーバー名（サーバーレベルで全サイトに適用する場合）または対象サイト（特定サイトのみの場合）を選択
2. 「URL書き換え」をダブルクリック →「操作」→「規則の追加」→「リバースプロキシ」
3. プロキシ先に`127.0.0.1:8000`（Waitressの待ち受けポート）を入力して適用
4. 生成されたInboundルールのパターンが`(.*)`、書き換え先が`http://127.0.0.1:8000/{R:1}`になっていることを確認
5. サーバーレベルで設定した場合はそのサーバー上の全サイトに、特定サイトで設定した場合はそのサイトのみに適用される

サイトを新規に追加する場合は「Sites」を右クリック→「Webサイトの追加」→サイト名・物理パス（空フォルダで可）・バインド（ポート80等）を設定。

## SSL/TLS証明書の取得

### 商用CAから購入する場合

1. IISマネージャー→サーバー証明書→「証明書要求の作成」でCSR（共通名・組織名・所在地等）を作成し`.csr`を保存
2. CA（DigiCert、GlobalSign、Sectigo等）にCSRをアップロードし、ドメイン所有確認（メール/DNS認証）後に証明書（`.cer`）を取得
3. IISマネージャー→サーバー証明書→「証明書要求の完了」で`.cer`を取り込み
4. 対象証明書を選択して「エクスポート」→パスワード設定の上`.pfx`として保存

### Let's Encrypt（無料・自動更新）+ win-acme

1. [win-acme公式](https://www.win-acme.com/)からZIPをダウンロードし解凍
2. 管理者権限で`wacs.exe`を実行し「Create new certificate (simple for IIS)」を選択
3. IIS登録済みサイト一覧からFlaskサイトを選択すると、HTTP-01によるドメイン認証→証明書取得→IISへのバインド→PFX生成まで自動実行される
4. 既定でWindows証明書ストアに格納。必要なら「Export Certificates」からPFXを書き出し可能

## アクセスログの実装

当初SQLite3でのアクセスログ記録を検討したが、最終的にはPostgreSQLを採用（[[postgresql|PostgreSQL運用メモ]]参照）。SQLite案は参考として残す。

**Windows Server環境での注意点**:
- ファイルパスは`os.path.join`でOS差異を吸収する
- SQLiteはファイルロックが厳しいため、複数プロセスの同時アクセスにはスレッドローカルストレージでDB接続を管理する
- `instance`ディレクトリの作成権限、Windowsサービス実行時はサービスアカウントへの権限付与を確認する

```
flask init-db              # データベースを再初期化（うまくいかない場合は python -m flask init-db）
flask export-logs --days 30  # 過去30日のログをCSVに出力
```

分析にはDB Browser for SQLite、SQLiteStudio等が利用できる。

## 本番環境に向けた改善ロードマップ

Windows10/Python3.9、Flask＋Waitress＋SQLiteの構成を前提に、堅牢性・拡張性・保守性・セキュリティを高める段階的な計画。

1. **永続化基盤の強化**: SQLite→PostgreSQL/MySQL移行（SQLAlchemy＋psycopg2等で接続プーリング）、Alembicでマイグレーション管理
2. **コンテナ化と環境分離**: Dockerfile化、docker-composeで開発スタック（DB・Redis等）を再現、python-dotenvで機密情報を分離
3. **CI/CDパイプライン構築**: pytest+coverageでテスト自動化、GitHub Actions等でPR時の自動テスト、flake8/black/mypyで静的解析、pre-commitフック
4. **監視・可観測性**: ログ集約（Fluentd/Logstash→Elasticsearch等）、構造化ログ（python-json-logger）、Prometheus+Grafanaでメトリクス可視化、Alertmanager等での異常通知
5. **セキュリティ強化**: Let's Encrypt+Nginx/IISでTLS化、Flask-LoginやOAuth2導入、CSRFトークン（Flask-WTF）・CSP/HSTS・ORM利用によるSQLインジェクション対策、Dependabot/Snykでの依存ライブラリ脆弱性スキャン
6. **パフォーマンステスト・チューニング**: Locust/JMeterでの負荷試験、Redisによるキャッシュ、cProfile+SnakeVizでのプロファイリング

推奨順序: ①DB移行＋マイグレーション整備 → ②Docker化＋CI/CD構築 → ③監視・アラート＋セキュリティ対策。

## LDAP認証のスキップ設定（開発時）

環境変数でLDAP認証の有無を切り替える。

```powershell
$env:SKIP_LDAP = 'true'   # スキップする
$env:SKIP_LDAP = 'false'  # スキップしない
python waitress_server.py
```

### 複数Flaskアプリの実装統一方針

`crud`と`pulldownlist`の2アプリで環境変数取得方法（直接取得 vs dotenv）、DB初期化、認証処理、エラーハンドリング等の書き方が異なっていたため、以下を統一してメンテナンス性を向上：環境変数の取得方法、DB初期化・接続処理、認証処理、エラーハンドリング、ディレクトリ構造の表記。

## 関連

- [[postgresql|PostgreSQL運用メモ]]
- [[Webサーバー運用メモ(IIS・Apache・FastAPI)|Webサーバー運用メモ（IIS・Apache・FastAPI）]]
- [[pediadose|PediaDose（個人開発Androidアプリ）]]
