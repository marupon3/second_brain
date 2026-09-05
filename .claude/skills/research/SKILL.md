---
name: query
description: Vault全体（wiki/を中心に）を対象に質問応答する。ユーザーが/queryを実行したときに使用する。
---

# query

## When to use

- ユーザーが `/query` で質問したとき

## When not to use

- 質問内容がVault内の知識と無関係なとき（一般的な質問はこのSkillを使わず直接回答する）

## Input

- ユーザーの質問文
- `wiki/` `obsidian_vault/daily/` `weekly/` 配下のページ

## Output

- 回答（会話内に出力）
- 必要に応じてユーザーの了承を得たうえで`wiki/`への保存

## 手順

1. 質問内容を解析し、関連しそうなキーワード・トピックを特定する。
2. `wiki/`を中心に、`obsidian_vault/daily/` `weekly/`も含めてファイルシステムを直接走査し、関連ページを横断的に探索する（インデックスは持たない、`docs/basic-design.md` 3.4節ADR-4）。
3. 関連ページの内容を統合して回答を作成し、参照元ページをwikilink（`[[ページ名]]`）で示す。
4. ユーザーが希望する場合のみ、回答を`wiki/`に新規ページとして保存する。このとき
   `memory/conventions.md`を読み、`wiki/`ページの規約（frontmatterの`title`/`updated`、
   `wiki/index.md`への追記、実在ページへのwikilink）を満たしてから保存する。
   保存しない場合はメモリを読む必要はない。

## 制約

- `obsidian_vault/raw/`配下のファイルを編集しない。
- `wiki/`へ保存する場合は`memory/conventions.md`の規約に従う（違反すると`/lint`が
  `INDEX_MISSING` `FRONTMATTER_MISSING_KEY` 等として検出する）。
- `memory/`配下のファイルをこのSkillから書き換えない。
- Vaultが大規模（千ページ超）な場合は、フォルダやタグで範囲を絞ったクエリを推奨する（`docs/requirements.md` 6節Q4）。
- 出力は日本語で書く。
- ファイル入出力時はエンコーディングを UTF-8 で明示する。
- コンソール出力以外で絵文字を使わない。
