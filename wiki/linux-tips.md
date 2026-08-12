---
title: Linux / Ubuntu Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Linux/2025-02-11 _Linuxにソフトウェアをインストール.md
  - obsidian_vault/raw/notes/Linux/2025-12-14 Linuxファイルシステム図解.md
  - obsidian_vault/raw/notes/Windows/2025-02-11 ＿Linux xubuntuパーティション.md
  - obsidian_vault/raw/notes/Tips/2025-03-24 Linuxディレクトリ構造.md
  - obsidian_vault/raw/pdfs/Exported image 20260807131801-0.png
---

# Linux / Ubuntu Tips

## ソフトウェアインストール（snap）

LibreOfficeはsnapで導入できる。

```
sudo snap install libreoffce
```

参考: <https://note.kurodigi.com/post-0-15/>

## Xubuntuのパーティション構成（デュアルブート用USB/SSD）

- `/dev/sdd1`: EFI、500MB
- `/dev/sdd2`: ext4
- ブートローダは`/dev/sdd`を指定

参考: <https://www.hayate-lab.net/usb_sdd-2/>

## Linuxディレクトリ構造（FHS）

| ディレクトリ | 説明 |
| --- | --- |
| `/bin` | 基本的なコマンドのプログラム（cat, mkdir, echo等）。Binaryの略 |
| `/boot` | システムの起動に必要なファイル |
| `/dev` | キーボードやマウス等デバイスのファイル・ディレクトリを保存。deviceの略 |
| `/etc` | 設定ファイル（システムの様々な設定）を保存 |
| `/home` | ユーザーのホームディレクトリ（デスクトップ等含む） |
| `/lib` | 共有ライブラリ（複数のプログラム間で共有されるライブラリ） |
| `/media` | USBやDVD等のリムーバブル媒体をマウント（OSが認識） |
| `/mnt` | ファイルシステムを一時的にマウント |
| `/opt` | 拡張アプリケーション、ソフトウェアパッケージ |
| `/proc` | カーネル関連の情報。仮想ファイルシステム（ディスク上でなくメモリ上に存在） |
| `/sbin` | システム管理者用のコマンド（rootユーザーのみ実行可） |
| `/srv` | システムが提供するデータ（HTTP、FTP用データ） |
| `/tmp` | 一時的なファイル（システム使用中に作られる臨時データ等） |
| `/usr` | 各ユーザーが共通して利用するプログラム |
| `/var` | ログファイルなど動的に変化するファイル。Variableの略 |

「Linuxファイルシステム図解」（2025-12-14）は本文未記入のノートだったが、`obsidian_vault/raw/pdfs/`に同内容の鮮明な図解画像が別途保存されていたため、上記の表はその画像を一次情報として作成した（`/proc`はカーネル情報にアクセスするための仮想ファイルシステム、`/run`はシステム実行中の一時ファイル格納先である点も含め内容を確認済み）。

## 関連ページ

- [[windows-tips|Windows Tips]]
