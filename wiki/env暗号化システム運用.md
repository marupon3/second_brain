---
title: .env暗号化システムの運用（webapp5/koneta）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2025-12-22 _暗号化システムのセットアップ.md
  - obsidian_vault/raw/notes/Python/2025-12-22 _暗号作成.md
  - "obsidian_vault/raw/notes/Python/2025-12-22 _暗号作成 (2).md"
  - obsidian_vault/raw/notes/Python/2025-12-22 _暗号の復号化.md
  - obsidian_vault/raw/notes/Python/2025-12-22 _暗号ファイルの編集.md
  - obsidian_vault/raw/notes/Python/2025-12-23 _.env暗号化操作マニュアル.md
  - obsidian_vault/raw/notes/Python/2026-01-08 _暗号化.md
  - obsidian_vault/raw/notes/Python/2026-01-08 _複合化.md
---

# .env暗号化システムの運用（webapp5/koneta）

DB接続情報やLDAP設定を含む`.env`ファイルをAES-256で暗号化して管理する自作の運用フロー（`webapp5`プロジェクト）。原文には実際に生成された暗号化キー（Base64文字列）が記載されていたが、秘密情報のため本ページには転記していない。

## セットアップ

```powershell
pip install cryptography --break-system-packages
python -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM; print('OK - cryptography installed')"
python generate_key.py
```

`generate_key.py`はAES-256の暗号化キーをBase64形式で生成し、以下いずれかの方法で保存を選べる。

1. Windows環境変数に保存（推奨）
2. ファイル（例: `.encryption_key`）に保存
3. 画面に表示のみ（手動でコピー）

生成されたキーを紛失すると暗号化した`.env`は復号できなくなるため、必ず安全な場所に保管する。

## 暗号化（`encrypt_env.py`）

```
python encrypt_env.py
```

`.env`のパスと出力先（既定`.env.encrypted`）を確認され、暗号化キーが未保存の場合は入力を求められる。暗号化完了後、セキュリティのため元の`.env`を削除するか確認される（推奨: 削除）。

## 復号化（`decrypt_env.py`）

```
python decrypt_env.py
```

出力方法を「画面表示」「`.env`として保存」「両方」から選択できる。復号した`.env`ファイルは機密情報を含むため、作業終了後は必ず削除する。

## 暗号ファイルの編集手順

1. `python decrypt_env.py` →「2: .envファイルとして保存」を選択して復号
2. PyCharm等で`.env`を編集
3. `python encrypt_env.py`で再暗号化（上書き確認・元ファイル削除確認ともに`y`）
4. `python waitress_server.py`で動作確認

作業前に`.env.encrypted`のバックアップを取ることを推奨（`copy .env.encrypted .env.encrypted.backup`）。

## 動作確認時のログ例

正常時は以下のようなログが出力される。

```
[INFO] app.database_manager: 環境設定読み込み成功: ...\.env.encrypted (暗号化ファイル)
```

## 関連

- 詳細な操作マニュアルは`env暗号化システム操作マニュアル.md`（PDF併存）として別途管理
- [[Flask本番運用ガイド(Windows・IIS・Waitress)|Flask本番運用ガイド（Windows・IIS・Waitress）]]
- [[nginx設定(koneta)|Nginx + Flask 本番環境構成（koneta）]]
