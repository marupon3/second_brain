---
title: second_brainのディレクトリ構成
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Obsidian/2026-08-07 obsidian-second-brain構成.md
  - obsidian_vault/raw/notes/Obsidian/2026-08-09 Cloud CodeでObsidianのWikiを作成する.md
---

# second_brainのディレクトリ構成

## フォルダ構成（2026-08-09時点）

```
second_brain/
├── .claude/
├── docs/
├── obsidian_vault/
│   ├── .obsidian/
│   ├── areas/
│   ├── daily/
│   ├── private/       # 人間のみ・gitignore対象（非公開情報）
│   ├── raw/
│   │   ├── articles/
│   │   ├── notes/
│   │   ├── pdfs/
│   │   └── personal/
│   ├── resources/
│   ├── templates/
│   └── ようこそ.md
├── scripts/
├── weekly/
├── wiki/
├── .env
├── .env.example
├── .gitignore
├── CLAUDE.md
├── obsidian-claude-guide.html
├── pyproject.toml
└── README.md
```

`obsidian_vault/ようこそ.md`は`raw/`・`daily/`などの下位分類フォルダに属さず、`obsidian_vault/`直下に置かれている。各フォルダの役割は[[CLAUDE.md|CLAUDE.md運用マニュアル]]（`obsidian_vault/`構造の節）を参照。

## `/ingest`の処理フロー

1. ユーザーがClaude Code CLI上で`/ingest`コマンドを実行する
2. `.claude/skills/ingest/SKILL.md`に定義された指示書（プロンプト）をClaudeが読み込む
3. Claude自身が`obsidian_vault/raw/`の新規ファイルをReadツールでAIとして読解し、要約・概念抽出・wikilink付与などを行い、`wiki/`にMarkdownファイルとしてAIが直接書き込む（Writeツール）
4. 併せて`wiki/index.md`・`wiki/log.md`も更新する

関連: [[Obsidian]]、[[セカンドブレイン]]
