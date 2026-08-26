**使い方はシンプルです。ユーザーが直接この2つを編集することは基本的にありません。**

## 仕組み

```
obsidian_vault/templates/weekly-review.md  ← 雛形（骨組みだけ）
              ↓ /weekly実行時に自動で使われる
weekly/2026-W35.md                          ← 実際に生成される週次レビュー
```

## 週次の運用手順

1. **毎週、Claude Code CLI上で `/weekly` を実行する**（このsecond_brainリポジトリで`claude`起動後にコマンド入力）
2. Claudeが自動で以下を行う：
   - 実行日を含むISO週番号を算出（例: 2026-08-26なら`2026-W35`）
   - 直近7日分の `obsidian_vault/daily/` のDaily Noteを収集
   - 完了/未完了タスクと「AI生成」セクションの主要トピックを要約
   - `obsidian_vault/templates/weekly-review.md`の雛形（下記4セクション）を使って`weekly/2026-W35.md`を新規作成、または既存なら更新
3. 生成された`weekly/2026-W35.md`を**Obsidianではなく、エディタやGit上で確認**（`weekly/`はVault外のため、Obsidianアプリからは見えません）

## テンプレートの中身（雛形）

```markdown
# {{year}} W{{week}} Weekly Review

## 今週のまとめ
## 完了したタスク
## 未完了・引き継ぎタスク
## 関連ページ
```

この4セクションが、`/weekly`実行のたびに自動で埋められます。

## 補足：なぜObsidianで見えないのか

`weekly/`（`wiki/`も同様）はリポジトリ直下にあり、ObsidianアプリのVaultルート（`obsidian_vault/`）の**外**にあります。これは意図的な設計で、Claude Code CLIが直接読み書きするAI運用専用フォルダという位置づけです（詳細は`CLAUDE.md`2節）。生成物を見たい場合は、エディタで`weekly/`フォルダを直接開くか、GitHubで確認してください。

## まとめ

| やること | やらないこと |
|---|---|
| 毎週`/weekly`をClaude Code上で実行する | `weekly-review.md`テンプレートを手動で編集する |
| 生成された`weekly/YYYY-Www.md`を読む | `weekly/`配下のファイルを手動で作成・編集する |

`obsidian_vault/daily/`（毎日の`/daily`実行）さえ続けていれば、`/weekly`は自動で正しい要約を作れます。