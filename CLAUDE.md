# CLAUDE.md — 第二の脳（Second Brain）運用マニュアル

Claude Codeがこのリポジトリで作業する際に、セッション開始時に必ず読むこと。

## 1. プロフィール

- ユーザーは日本語話者。プロンプト・ノート・ファイル名はすべて日本語を標準とする。
- 本Vaultは個人用の知識管理システムであり、複数ユーザーでの共有は想定しない。
- 対象環境: Windows 11 / Python 3.11.9 / UTF-8。

## 2. フォルダ構造

`obsidian_vault/` は、ユーザーが新たに情報を追加するフォルダ（raw/daily/projects/areas/resources）をまとめた配下ディレクトリ。Obsidianのvault自体はリポジトリ直下（`second_brain/`）を開くため、`wiki/` `weekly/` `templates/`とあわせて同一Vault内で扱われる。

| フォルダ | 管理者 | 役割 |
|---|---|---|
| `obsidian_vault/raw/` | 人間のみ | 不変の原文・スクラップ。articles/notes/pdfs/personalに分類 |
| `wiki/` | AI | `obsidian_vault/raw/`から生成した要約・概念・エンティティページ。index.md/log.mdを含む |
| `obsidian_vault/daily/` | 人間+AI | 日次ノート（セクション分離: 人間メモ/AI生成/タスク） |
| `weekly/` | AI | 週次レビュー（`/weekly`で生成） |
| `obsidian_vault/projects/` `obsidian_vault/areas/` `obsidian_vault/resources/` | 人間+AI | 補助的な整理用フォルダ |
| `obsidian_vault/private/` | 人間のみ | パスワード等の非公開情報を含むローカル専用ノート。`.gitignore`で除外され、リモートには一切push・同期しない |
| `templates/` | 人間+AI | Daily Note等の固定テンプレート |
| `.claude/skills/` | - | カスタムSkills定義 |
| `memory/` | AI+人間 | Skillsが実行のたびに読む規約と、その学習履歴。Vaultの中身ではなく「Vaultを作る側のルール」を置く（詳細は`memory/index.md`） |
| `scripts/` | - | Python 3.11.9によるセットアップ・環境チェック・Vault検査用ユーティリティ |

## 3. 書き方ルール

- 日本語での記述を優先する。
- ページ間の関連は必ずObsidian形式のwikilink（`[[ページ名]]`）で表現する。
- すべてのMarkdownファイルはUTF-8で保存する。
- `wiki/`配下の新規・更新ページは、生成のたびに`wiki/index.md`と`wiki/log.md`を更新する。
- **`/ingest` `/daily` `/weekly` を実行する際は、手順に入る前に`memory/conventions.md`を読み、
  そこに書かれた規約に従う。** 本書に書かれていなくても、`memory/conventions.md`に載っている
  規約は守ること。規約の遵守は`python scripts/lint_vault.py`が違反コード付きで機械的に判定する。

## 4. 禁止事項

- **`obsidian_vault/raw/`配下のファイルはAIが編集・削除してはならない**。`obsidian_vault/raw/`は人間のみが書き込む不変ソースである。
- 破壊的操作（ファイルの削除・大規模な書き換え）は、実行前に必ずユーザーに確認を取ること。無断で実行しない。
- APIキー等の秘密情報をMarkdownファイルやコード中に直接書き込まない（`.env`または環境変数を使うこと）。
- `obsidian_vault/private/`配下の内容を`wiki/`等のコミット対象ファイルに転記・引用しない（パスワード等の非公開情報が漏洩するため）。
- `/lint`が検出した問題を無断で自動修正しない（検出・報告のみとする方針、`docs/requirements.md` 6節Q3）。
- **`memory/conventions.md`・`memory/lessons.md`を、ユーザーの明示的な承認なしに書き換えない。**
  ここへの追記は以後すべての実行に影響するため、`/dream`が提案し、人間が承認したものだけを反映する
  （誤った規約が入ると、以後の全生成物がその誤りに引きずられるため）。
- `/lint`が検出した違反を「誤検知」として黙って無視しない。仕様側が誤っていると判断した場合は、
  `memory/conventions.md`と検査ロジックの双方を直す。

## 5. 優先するSkills

初期実装で確定しているSkillsは以下の5つ（`docs/basic-design.md` 3.2節）。

- `/ingest` : `obsidian_vault/raw/`の新規ファイルを読み、`wiki/`に構造化ページを生成する
- `/daily` : 今日のDaily Noteを生成・更新する
- `/weekly` : 週次のWeekly Reviewを`weekly/`に生成・更新する
- `/lint` : リンク切れ・矛盾・孤立ページ・規約違反を検出し報告する（自動修正はしない）
- `/query` : Vault全体を対象に質問応答する

これに加えて、規約を育てるためのSkillを1つ持つ。

- `/dream` : `/lint`が記録した違反を横断的に読み、繰り返し起きている問題を
  `memory/conventions.md`の規約へ昇格する提案を出す。**既定では提案のみで、適用には
  ユーザーの明示的な承認を要する。**

いずれも手動コマンド実行がトリガーであり、スケジュール実行は行わない（`docs/requirements.md` 6節Q2）。

## 6. 学習ループ

`/lint`が検出した違反を`/dream`が規約へ昇格し、次回以降の`/ingest`がその規約を守った状態から
始まる、という1本のループを持つ。

```
/ingest /daily /weekly     memory/conventions.md を読んで生成する
      ↓
/lint                      違反を決定的に検出し memory/violations.jsonl へ記録する
      ↓
/dream                     何回の実行で再発したかを数え、規約への昇格を提案する
      ↓
人間が承認                 conventions.md へ追記し、記録を消化済みへ退避する
      ↓
次回の /ingest が、その規約を守った状態から始まる
```

合否判定の経路にLLMを置かないことがこのループの前提である。違反の検出（`scripts/lint_vault.py`）と
再発回数の集計（`scripts/dream_memory.py`）はいずれも決定的なスクリプトが担当し、これらの判定
ロジック本体はGrowLoop（`marupon3/GrowLoop`）でテスト駆動生成・検証された純粋関数である。
LLMが担うのは「規約としてどう書くか」の文言起こしだけで、適用には人間の承認を要する。
