---
name: weekly
description: 週次のWeekly Reviewをweekly/に生成・更新する。直近7日分のDaily Noteを要約する。ユーザーが/weeklyを実行したときに使用する。
---

# weekly

## When to use

- ユーザーが `/weekly` を実行したとき

## When not to use

- 対象週のobsidian_vault/daily/ノートが1件も存在しないとき

## Input

- `obsidian_vault/daily/` 配下の直近7日分のノート
- `memory/conventions.md` `memory/lessons.md`（生成物が守るべき規約。「メモリ」節を参照）

## Output

- `weekly/YYYY-Www.md`（例: `weekly/2026-W32.md`、ISO週番号）

## メモリ

手順に入る前に、必ず`memory/conventions.md`と`memory/lessons.md`を読む。ここに書かれた
規約は、生成物が満たすべき機械的に検証できる条件を定めたもので、守られているかどうかは
`/lint`（`scripts/lint_vault.py`）が決定的に判定する。

## 手順

1. 実行日を含むISO週の年・週番号を求める。
2. 対象週に含まれる`obsidian_vault/daily/`ノート（直近7日分）を収集する。
3. 完了・未完了タスク、`## AI生成`セクションの主要トピックを要約する。
4. `weekly/YYYY-Www.md`にWeekly Reviewページを生成・更新する（既存の場合は現在の内容を確認してから更新する）。
5. `wiki/log.md`に実行結果（対象週・参照した日次ノート数）を記録する。

## 制約

- `obsidian_vault/daily/`配下のノートを編集しない（読み取りのみ）。
- `obsidian_vault/raw/`配下のファイルを編集しない。
- `memory/conventions.md`の規約に反するページを生成しない。特に`title`と`updated`を含む
  frontmatter（`FRONTMATTER_MISSING_KEY` `FRONTMATTER_BAD_DATE`）と、実在ページへの
  wikilink（`BROKEN_LINK`）を必ず満たす。
- `memory/`配下のファイルをこのSkillから書き換えない（規約の更新は`/dream`と人間の承認を経る）。
- スケジュール実行は行わない。手動コマンド実行のみをトリガーとする（`docs/requirements.md` 6節Q2）。
- 出力は日本語で書く。
- ファイル入出力時はエンコーディングを UTF-8 で明示する。
- コンソール出力以外で絵文字を使わない。
