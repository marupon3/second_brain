---
title: Gitコマンド Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Tips/2026-01-22 _git設定方法.md
  - obsidian_vault/raw/notes/Tips/2026-06-26 _ローカルからPUSHするgitコマンド.md
  - obsidian_vault/raw/notes/Python/2025-04-20 git設定.md
  - obsidian_vault/raw/notes/Python/2025-07-23 _gitから除外.md
---

# Gitコマンド Tips

## フォルダ階層を丸ごとGit管理下に置く手順

1. 対象フォルダに移動: `cd C:\project`
2. リポジトリ初期化: `git init`（サブフォルダ・孫フォルダを含め自動で管理対象になる。個別設定は不要）
3. 現在のファイルを登録: `git add .`
4. 初回コミット: `git commit -m "Initial commit"`

以降の更新: `git status`で変更確認 → `git add .` → `git commit -m "変更内容の説明"`。除外したいファイル・フォルダは`.gitignore`を作成して指定（例: `node_modules/`、`*.log`、`temp/`）。

## ローカルからリモートへのPUSH例

```
git add local_to_Remote.txt
git commit -m "Update local_to_Remote.txt"
git push origin <branch名>
```

## PyCharmでのGit初期化とコミット（GUI操作）

1. PyCharmのターミナルで対象フォルダに移動し`git init`
2. 左側ウィンドウで対象ファイルを右クリック →「Git」→「ファイルの追加（+追加）」
3. 左側ウィンドウで「コミット」を選択 → ファイルを選択 → コメント入力 →「コミット」ボタン

## .gitignoreで特定フォルダをGit管理から除外する

```
# .gitignore に対象フォルダを追記（例: venv）
venv/
```

既にコミット済みのフォルダを後から除外する場合はステージングからも削除する。

```
git rm -r --cached venv
git commit -m "venv"
```

特定ファイル1件のみを追跡から外す場合:

```
git rm --cached app/rebuild_manager.py
```
