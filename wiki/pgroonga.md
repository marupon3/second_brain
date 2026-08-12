---
title: PGroonga（PostgreSQL全文検索）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/高速検索/2025-03-06 _pgroongaインストール.md
  - obsidian_vault/raw/notes/Python/2025-06-07 _Mecabとユーザ辞書の設定.md
---

# PGroonga（PostgreSQL全文検索）

## 概要

PGroongaはPostgreSQL向けのテキスト全文検索用拡張機能。日本語形態素解析（MeCab）に対応する。

## インストール手順（Windows / PostgreSQL 17）

1. [pgroonga-4.0.1-postgresql-17-x64.zip](https://github.com/pgroonga/pgroonga/releases/download/4.0.1/pgroonga-4.0.1-postgresql-17-x64.zip)をダウンロード
2. Zipを展開し、`C:\Program Files\PostgreSQL\17\`配下の各フォルダにコピー
3. `psql -U postgres -d <db名>`で接続し、`CREATE EXTENSION pgroonga;`を実行

参考: <https://pgroonga.github.io/install/windows.html>

## 日本語全文検索インデックス作成例

```sql
CREATE TABLE IF NOT EXISTS file_index (
    id SERIAL PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    content_hash BYTEA NOT NULL,
    content_text TEXT,
    last_indexed TIMESTAMP DEFAULT NOW(),
    encoding VARCHAR(20)
);

CREATE EXTENSION IF NOT EXISTS pgroonga;

CREATE INDEX IF NOT EXISTS idx_content_search
ON file_index USING pgroonga (content_text)
WITH (tokenizer='TokenMecab', normalizer='NormalizerAuto');
```

MeCabトークナイザとNormalizerAutoノーマライザにより、日本語テキストの全文検索インデックスを構築する。

## MeCabとユーザ辞書の設定（fulltextsearchプロジェクト）

- MeCab実行ファイル: `C:\Program Files\PostgreSQL\17\bin\mecab.exe`
- 辞書: `bin\dic\ipadic`配下（`dic`直下のipadicが基本）
- ユーザー辞書: プロジェクト内`fulltextsearch\user.dic`に配置
- `mecabrc`の位置: `bin\mecabrc`または`etc\mecabrc`（見つからない場合はMeCabインストール先を探す）

## 関連ページ

- [[postgresql|PostgreSQL運用メモ]]
- [[Python自然言語処理ライブラリ一覧]]
