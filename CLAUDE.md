# CLAUDE.md — 第二の脳（Second Brain）運用マニュアル

Claude Codeがこのリポジトリで作業する際に、セッション開始時に必ず読むこと。

## 1. プロフィール

- ユーザーは日本語話者。プロンプト・ノート・ファイル名はすべて日本語を標準とする。
- 本Vaultは個人用の知識管理システムであり、複数ユーザーでの共有は想定しない。
- 対象環境: Windows 11 / Python 3.11.9 / UTF-8。

## 2. フォルダ構造

| フォルダ | 管理者 | 役割 |
|---|---|---|
| `raw/` | 人間のみ | 不変の原文・スクラップ。articles/notes/pdfs/personalに分類 |
| `wiki/` | AI | `raw/`から生成した要約・概念・エンティティページ。index.md/log.mdを含む |
| `daily/` | 人間+AI | 日次ノート（セクション分離: 人間メモ/AI生成/タスク） |
| `weekly/` | AI | 週次レビュー（`/weekly`で生成） |
| `projects/` `areas/` `resources/` `templates/` | 人間+AI | 補助的な整理用フォルダ |
| `.claude/skills/` | - | カスタムSkills定義 |
| `scripts/` | - | Python 3.11.9によるセットアップ・環境チェック用ユーティリティ |

## 3. 書き方ルール

- 日本語での記述を優先する。
- ページ間の関連は必ずObsidian形式のwikilink（`[[ページ名]]`）で表現する。
- すべてのMarkdownファイルはUTF-8で保存する。
- `wiki/`配下の新規・更新ページは、生成のたびに`wiki/index.md`と`wiki/log.md`を更新する。

## 4. 禁止事項

- **`raw/`配下のファイルはAIが編集・削除してはならない**。`raw/`は人間のみが書き込む不変ソースである。
- 破壊的操作（ファイルの削除・大規模な書き換え）は、実行前に必ずユーザーに確認を取ること。無断で実行しない。
- APIキー等の秘密情報をMarkdownファイルやコード中に直接書き込まない（`.env`または環境変数を使うこと）。
- `/lint`が検出した問題を無断で自動修正しない（検出・報告のみとする方針、`docs/requirements.md` 6節Q3）。

## 5. 優先するSkills

初期実装で確定しているSkillsは以下の5つ（`docs/basic-design.md` 3.2節）。

- `/ingest` : `raw/`の新規ファイルを読み、`wiki/`に構造化ページを生成する
- `/daily` : 今日のDaily Noteを生成・更新する
- `/weekly` : 週次のWeekly Reviewを`weekly/`に生成・更新する
- `/lint` : リンク切れ・矛盾・孤立ページを検出し報告する
- `/query` : Vault全体を対象に質問応答する

いずれも手動コマンド実行がトリガーであり、スケジュール実行は行わない（`docs/requirements.md` 6節Q2）。
