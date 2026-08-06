# second-brain

Claude Code（Claude Codeエージェント）とObsidianを組み合わせた個人用の「第二の脳（Second Brain）」。
`raw/`に投入した生データから、AIが`wiki/`に構造化知識を継続的に生成・維持する、ローカル完結型の知識管理システム。
対象利用者は本Vaultを日常的に使う個人（単一ユーザー）。

## 前提環境

- OS: Windows 11（64bit）
- Python: 3.11.9（厳密固定。`pyproject.toml`の`requires-python`で指定）
- パッケージ管理: `uv`（主）、`pip`（フォールバック）
- Git
- Node.js（一部のClaude Code関連ツールで必要な場合のみ）
- Claude Code（Pro以上のプラン）
- Obsidian（最新安定版）

## セットアップ手順

1. 依存ツールの確認

   ```
   python scripts/check_env.py
   ```

   Python 3.11.9・Git・uv・pipが揃っているか確認する。不足があるとメッセージが表示され、終了コード1で終了する。

2. Vaultディレクトリ構造の生成

   ```
   python scripts/setup.py
   ```

   `raw/` `wiki/` `daily/` `weekly/` 等のディレクトリ構造を生成する（既存のファイル・ディレクトリは上書きしない）。カレントディレクトリ以外に生成したい場合は対象ディレクトリを引数で指定する。

   ```
   python scripts/setup.py C:\path\to\target
   ```

3. CLAUDE.mdを確認・カスタマイズする

   `CLAUDE.md`にAIの運用ルール（プロフィール・フォルダ構造・書き方ルール・禁止事項・優先Skills）が定義されている。必要に応じて内容を編集する。

4. Obsidianでこのフォルダを開く

   Obsidianの「フォルダを開く」からこのディレクトリを指定する。

5. Claude Codeをこのディレクトリで起動する

   ```
   cd second_brain
   claude
   ```

## 環境変数

現時点で必須の環境変数はない。将来的にMCPサーバー等が外部APIキーを必要とする場合は、`.env.example`をコピーして`.env`を作成し、値を設定すること（`.env`はコミットしない）。

```
copy .env.example .env
```

## 起動・利用コマンド

ビルドやテストの手順は無い（Markdownベースの知識ベースであり、ビルド成果物を持たない）。日常利用はClaude Code上でのSkills実行が中心となる。

- `/ingest` : `raw/`の新規ファイルを`wiki/`に構造化
- `/daily` : Daily Noteを生成・更新
- `/weekly` : Weekly Reviewを生成・更新
- `/lint` : リンク切れ・矛盾・孤立ページを検出（自動修正は行わない）
- `/query` : Vault全体を対象に質問応答

## ディレクトリ構成の要点

```
second_brain/
├── CLAUDE.md          # AI運用マニュアル
├── raw/                # 不変ソース（人間のみ編集）
├── wiki/                # AI生成知識ベース
├── daily/               # 日次ノート
├── weekly/              # 週次レビュー
├── projects/ areas/ resources/ templates/
├── .claude/skills/       # カスタムSkills定義
└── scripts/              # 環境チェック・セットアップ用スクリプト
```

詳細なディレクトリ設計・Skills仕様は本Vaultの設計元となった基本設計書を参照（本リポジトリには同梱していない）。
