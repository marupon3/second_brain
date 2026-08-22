---
title: second_brainのディレクトリ構成
updated: 2026-08-22
source:
  - obsidian_vault/raw/notes/Obsidian/2026-08-07 obsidian-second-brain構成.md
  - obsidian_vault/raw/notes/Obsidian/2026-08-09 Cloud CodeでObsidianのWikiを作成する.md
---

# second_brainのディレクトリ構成

## フォルダ構成（2026-08-22時点）

```
second_brain/
├── .claude/
│   ├── hooks/         # PreToolUse Hooks: 破壊的操作・秘密情報書き込み防止
│   │   ├── block-dangerous-git.sh     # git push --force / reset --hard / clean -f / checkout . / branch -D ブロック
│   │   ├── block-raw-bash.sh          # raw/ 対象の rm / mv / sed -i 等ブロック
│   │   ├── block-raw-edit.sh          # raw/ への Edit/Write/NotebookEdit ブロック
│   │   └── block-secret-write.sh      # APIキー（Google/Anthropic/GitHub/AWS/OpenAI）パターン検知・ブロック
│   ├── settings.json   # Hook登録・permissions設定
│   └── skills/        # daily / ingest / lint / query / weekly
├── obsidian_vault/    # ObsidianアプリのVaultルート
│   ├── .obsidian/
│   ├── daily/
│   ├── private/       # 人間のみ・gitignore対象（非公開情報）
│   ├── raw/
│   │   ├── articles/
│   │   ├── notes/
│   │   ├── pdfs/
│   │   └── personal/
│   ├── templates/
│   └── ようこそ.md
├── scripts/
├── weekly/            # Vault外・AI運用専用
├── wiki/              # Vault外・AI運用専用
├── .env
├── .env.example
├── .gitignore
├── CLAUDE.md
├── obsidian-claude-guide.html
├── pyproject.toml
└── README.md
```

`obsidian_vault/ようこそ.md`は`raw/`・`daily/`などの下位分類フォルダに属さず、`obsidian_vault/`直下に置かれている。各フォルダの役割は[[CLAUDE.md|CLAUDE.md運用マニュアル]]（`obsidian_vault/`構造の節）を参照。

ObsidianアプリのVaultルートは`obsidian_vault/`であり、リポジトリ直下ではない（`.obsidian/`が`obsidian_vault/`配下にのみ存在する）。そのため`wiki/`・`weekly/`はObsidianアプリからは見えず、wikilinkも解決されない。両フォルダはClaude Code CLI（Skills）が直接読み書きするAI運用専用ディレクトリという位置づけ。

過去に存在した`docs/`・`obsidian_vault/areas/`・`obsidian_vault/resources/`は廃止済み（`projects/`は実体として作られたことがない）。

## `/ingest`の処理フロー

1. ユーザーがClaude Code CLI上で`/ingest`コマンドを実行する
2. `.claude/skills/ingest/SKILL.md`に定義された指示書（プロンプト）をClaudeが読み込む
3. Claude自身が`obsidian_vault/raw/`の新規ファイルをReadツールでAIとして読解し、要約・概念抽出・wikilink付与などを行い、`wiki/`にMarkdownファイルとしてAIが直接書き込む（Writeツール）
4. 併せて`wiki/index.md`・`wiki/log.md`も更新する

関連: [[Obsidian]]、[[セカンドブレイン]]
