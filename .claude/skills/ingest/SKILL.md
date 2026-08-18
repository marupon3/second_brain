---
name: ingest
description: obsidian_vault/raw/の新規ファイル（記事・メモ・PDF等）を読み、wiki/に構造化されたページを生成する。ソースを投入した直後、ユーザーが/ingestを指示したときに使用する。
---

# ingest

## When to use

- `obsidian_vault/raw/`（`articles/` `notes/` `pdfs/` `personal/`）に新しいソースが投入されたとき
- ユーザーが `/ingest` を実行したとき

## When not to use

- `obsidian_vault/raw/`に未処理の新規ファイルが無いとき

## Input

- `obsidian_vault/raw/articles/` `obsidian_vault/raw/notes/` `obsidian_vault/raw/pdfs/` `obsidian_vault/raw/personal/` 配下の未処理ファイル

## Output

- `wiki/` 配下の新規ページ、または既存ページの更新
- `wiki/index.md`（生成・更新したページへのリンク追記）
- `wiki/log.md`（実行結果の記録）

## 手順

1. `obsidian_vault/raw/`配下を確認し、`wiki/log.md`にまだ記録の無い未処理ファイルを特定する。
2. ファイル種別に応じて内容を読み取る。
   - テキスト・Markdown・記事: 全文をそのまま解析対象とする。
   - PDF: **テキスト抽出のみ**を構造化対象とする。画像・図表はデフォルトで保持せず、必要に応じて説明文（キャプション相当）のみをテキストとして記載する。埋め込みリンクはURLをテキストとして抽出し、関連ページへの参照として記録する。
3. 内容を要約・構造化し、`wiki/`にYAML frontmatter付きのMarkdownページとして新規作成、または関連する既存ページを更新する。ページ間の関連は必ずObsidian形式のwikilink（`[[ページ名]]`）で表現する。
4. 生成・更新したページへのリンクを`wiki/index.md`に追記する。
5. 実行結果（日時・対象ファイル・生成/更新したページ）を`wiki/log.md`に追記する。

## 制約

- `obsidian_vault/raw/`配下のファイルは読み取りのみとし、一切編集・削除しない（`CLAUDE.md` 4節 禁止事項）。
- PDFの画像・図表本体をwiki側に保持する機能は今回のスコープに含めない（将来拡張）。
- 千ページ超の大規模Vaultでは処理対象を絞ることを検討する（性能目安: 1件あたり30〜90秒）。
- 出力は日本語で書く。
- ファイル入出力時はエンコーディングを UTF-8 で明示する。
- コンソール出力以外で絵文字を使わない。
