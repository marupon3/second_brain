---
name: daily
description: 今日のDaily Noteをobsidian_vault/daily/に生成・更新する。人間メモ/AI生成/タスクのセクションに分離し、人間が編集したセクションは上書きしない。ユーザーが/dailyを実行したときに使用する。
---

# daily

## When to use

- ユーザーが `/daily` を実行したとき

## When not to use

- 該当日のDaily Noteが既に存在し、追記すべき新しい内容が無いとき

## Input

- `obsidian_vault/daily/` 配下の当日ノート（存在する場合）
- `obsidian_vault/templates/daily-note.md`（新規作成時のテンプレート）

## Output

- `obsidian_vault/daily/YYYY-MM-DD.md`

## 手順

1. 当日の日付で`obsidian_vault/daily/YYYY-MM-DD.md`が存在するか確認する。
2. 存在しない場合は`obsidian_vault/templates/daily-note.md`を元に新規作成する。
3. 存在する場合は、更新前に必ず現在の内容を読み込んでから更新する。
4. 「## 人間メモ」セクションの内容は変更しない。
5. 「## AI生成」セクションと「## タスク」セクション（前日までの未完了タスクの引き継ぎ）を追記・更新する。
6. 同一セクション内で内容が競合する場合は、後から書き込んだ内容を優先する（後勝ち）。履歴確認はGitコミットで行う。

## 制約

- 「## 人間メモ」セクションを上書き・削除しない。
- `obsidian_vault/raw/`配下のファイルを編集しない。
- 出力は日本語で書く。
- ファイル入出力時はエンコーディングを UTF-8 で明示する。
- コンソール出力以外で絵文字を使わない。
