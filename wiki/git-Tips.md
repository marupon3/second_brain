---
title: Gitコマンド Tips
updated: 2026-08-13
source:
  - obsidian_vault/raw/notes/Tips/2026-01-22 _git設定方法.md
  - obsidian_vault/raw/notes/Tips/2026-06-26 _ローカルからPUSHするgitコマンド.md
  - obsidian_vault/raw/notes/Python/2025-04-20 git設定.md
  - obsidian_vault/raw/notes/Python/2025-07-23 _gitから除外.md
  - obsidian_vault/raw/notes/Githubのリポジトリ容量の削減.md
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

## GitHubリポジトリの容量を確認・削減する

複数リポジトリのディスク使用量は`gh`コマンドで一覧できる。

```powershell
gh repo list <ユーザー名> --limit 200 --json name,diskUsage |
  ConvertFrom-Json |
  ForEach-Object { "$($_.name): $($_.diskUsage) KB" }
```

容量削減は影響範囲が小さい順に3段階で検討する。

1. **Git LFS導入（今後の肥大化防止）**: 大きなバイナリ（画像・PDF等）を今後もコミットし続ける場合に有効。既存の履歴は軽くならない。

   ```powershell
   git lfs install
   git lfs track "*.png"
   git lfs track "*.jpg"
   git lfs track "*.jpeg"
   git lfs track "*.pdf"
   git add .gitattributes
   git commit -m "Enable LFS for large files"
   git push
   ```

2. **BFG Repo-Cleaner / git-filter-repoで履歴から巨大ファイルを削除（容量削減の本丸）**: 過去のコミット履歴自体から不要な大容量ファイルを除去する。実行後は`git push --force`が必要になるため、共同作業中のリポジトリでは事前調整が必須。

   ```powershell
   bfg --delete-files *.png
   bfg --delete-files *.jpg
   # 特定フォルダを丸ごと削除する場合
   pip install git-filter-repo
   git filter-repo --path assets --invert-paths
   # BFG実行後
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

3. **履歴ごと初期化（最終手段・容量をほぼゼロにする）**: 巨大ファイルが大量にある場合に最も確実だが、コミット履歴が完全に失われる。

   ```powershell
   git checkout --orphan latest_branch
   git add -A
   git commit -m "Initial clean commit"
   git branch -D main
   git branch -m main
   git push -f origin main
   ```
