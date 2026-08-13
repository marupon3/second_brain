---
title: Windows Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Windows/2025-02-15 _Windows起動時に時間を同期.md
  - obsidian_vault/raw/notes/Windows/2025-02-17 _OneNote便利機能.md
  - obsidian_vault/raw/notes/Windows/2025-03-29 _prefetch最適化.md
---

# Windows Tips

## 起動時に時刻を自動同期する

タスクスケジューラで起動時にNTP時刻同期を自動実行する設定。

1. タスクスケジューラ（`taskschd.msc`）を開く
2. 「基本タスクの作成」→ トリガー「コンピューターの起動時」
3. 操作「プログラムの開始」: `C:\Windows\System32\w32tm.exe`、引数`/resync /force`
4. プロパティのセキュリティオプションで「最上位の特権で実行する」を有効化、構成は「Windows 11」

Windows Timeサービスが起動している必要がある。

## OneNote便利機能

- 複数のテキストボックスを結合: `Shift + ドラッグ`
- 箇条書きに変換: `Ctrl + .`
- チェックボックス挿入: `Ctrl + 1`
- テキスト強調: `Ctrl + Shift + H` / `Ctrl + 4` / `Ctrl + 5`

参考: <https://forest.watch.impress.co.jp/docs/serial/offitech/1663115.html>

## Prefetch/Superfetch設定

レジストリ `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters` の`EnablePrefetcher`/`EnableSuperfetch`で制御（Win11に`EnableSuperfetch`は無い）。

| 値 | 意味 |
| --- | --- |
| 0 | 機能を無効化 |
| 1 | アプリケーションを有効化 |
| 2 | システムを有効化 |
| 3 | 初期値（システム・アプリケーション両方有効） |

参考: <https://jisaku-pc.net/speed/reji_03.html>

## 関連ページ

- [[linux-tips|Linux / Ubuntu Tips]]
