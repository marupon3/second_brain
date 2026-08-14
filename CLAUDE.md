# CLAUDE.md — 第二の脳（Second Brain）運用マニュアル

Claude Codeがこのリポジトリで作業する際に、セッション開始時に必ず読むこと。

## 1. プロフィール

- ユーザーは日本語話者。プロンプト・ノート・ファイル名はすべて日本語を標準とする。
- 本Vaultは個人用の知識管理システムであり、複数ユーザーでの共有は想定しない。
- 対象環境: Windows 11 / Python 3.11.9 / UTF-8。

## 1.1 回答方針（必須）

- 本プロジェクトでのやり取りでは、回答前に必ず`wiki/`（Obsidian Wiki）の関連ページを参照すること。
- Wikiの内容を回答の基盤としつつ、通常の生成AIとしての知識・推論も併用し、不足やギャップを補うこと。
- Wikiに情報がない場合でも、その旨を明示した上で通常の知識で回答してよい。

## 2. フォルダ構造

`obsidian_vault/` は、ユーザーが新たに情報を追加するフォルダ（raw/daily/templates）をまとめた配下ディレクトリ。Obsidianのvault自体はリポジトリ直下（`second_brain/`）を開くため、`wiki/` `weekly/`とあわせて同一Vault内で扱われる。

| フォルダ | 管理者 | 役割 |
|---|---|---|
| `obsidian_vault/raw/` | 人間のみ | 不変の原文・スクラップ。articles/notes/pdfs/personalに分類 |
| `wiki/` | AI | `obsidian_vault/raw/`から生成した要約・概念・エンティティページ。index.md/log.mdを含む |
| `obsidian_vault/daily/` | 人間+AI | 日次ノート（セクション分離: 人間メモ/AI生成/タスク） |
| `weekly/` | AI | 週次レビュー（`/weekly`で生成） |
| `obsidian_vault/private/` | 人間のみ | パスワード等の非公開情報を含むローカル専用ノート。`.gitignore`で除外され、リモートには一切push・同期しない |
| `obsidian_vault/templates/` | 人間+AI | Daily Note等の固定テンプレート |
| `.claude/skills/` | - | カスタムSkills定義 |
| `scripts/` | - | Python 3.11.9によるセットアップ・環境チェック用ユーティリティ |

## 3. 書き方ルール

- 日本語での記述を優先する。
- ページ間の関連は必ずObsidian形式のwikilink（`[[ページ名]]`）で表現する。
- すべてのMarkdownファイルはUTF-8で保存する。
- `wiki/`配下の新規・更新ページは、生成のたびに`wiki/index.md`と`wiki/log.md`を更新する。

## 4. 禁止事項

- **`obsidian_vault/raw/`配下のファイルはAIが編集・削除してはならない**。`obsidian_vault/raw/`は人間のみが書き込む不変ソースである。
- 破壊的操作（ファイルの削除・大規模な書き換え）は、実行前に必ずユーザーに確認を取ること。無断で実行しない。
- APIキー等の秘密情報をMarkdownファイルやコード中に直接書き込まない（`.env`または環境変数を使うこと）。
- `obsidian_vault/private/`配下の内容を`wiki/`等のコミット対象ファイルに転記・引用しない（パスワード等の非公開情報が漏洩するため）。
- `/lint`が検出した問題を無断で自動修正しない（検出・報告のみとする方針、`docs/requirements.md` 6節Q3）。

## 5. 優先するSkills

初期実装で確定しているSkillsは以下の5つ（`docs/basic-design.md` 3.2節）。

- `/ingest` : `obsidian_vault/raw/`の新規ファイルを読み、`wiki/`に構造化ページを生成する
- `/daily` : 今日のDaily Noteを生成・更新する
- `/weekly` : 週次のWeekly Reviewを`weekly/`に生成・更新する
- `/lint` : リンク切れ・矛盾・孤立ページを検出し報告する
- `/query` : Vault全体を対象に質問応答する

いずれも手動コマンド実行がトリガーであり、スケジュール実行は行わない（`docs/requirements.md` 6節Q2）。
