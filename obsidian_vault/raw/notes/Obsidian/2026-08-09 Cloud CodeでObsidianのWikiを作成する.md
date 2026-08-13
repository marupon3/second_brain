---
"Date Created:": 2026-08-09
"updated:": 2026-08-09
---
# Wiki作製手順

1. ユーザーが Claude Code CLI 上で `/ingest` コマンドを実行する
2. これは [`.claude/skills/ingest/SKILL.md`](https://github.com/marupon3/second_brain/blob/claude/sync-local-to-github-zyskxk/.claude/skills/ingest/SKILL.md) に定義された指示書（プロンプト）を Claude が読み込む
3. Claude自身が `obsidian_vault/raw/` の新規ファイルをReadツールで**AIとして読解**し、要約・概念抽出・wikilink付与などを行い、`wiki/` にMarkdownファイルとして**AIが直接書き込む**（Writeツール）
4. 併せて [`wiki/index.md`](https://github.com/marupon3/second_brain/blob/claude/sync-local-to-github-zyskxk/wiki/index.md) [`wiki/log.md`](https://github.com/marupon3/second_brain/blob/claude/sync-local-to-github-zyskxk/wiki/log.md) も更新する
 
