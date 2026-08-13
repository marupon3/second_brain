---
title: PCクリーナーアプリ Kudu
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Tips/2026-07-22 cleaner アプリ.md
---

# PCクリーナーアプリ Kudu

CCleanerの無料オープンソース代替として紹介されたツール。AdventDevチームが開発。Windows/macOS/Linux対応（Intel・Apple Siliconビルドあり）、広告・アップセル・テレメトリ・アカウント登録なし、MITライセンス。

## 主な機能

- システムクリーナー（テンポラリファイル・ログ・キャッシュ・クラッシュダンプ）
- ブラウザクリーナー（主要ブラウザ対応）
- ゲーミングクリーナー（ランチャー・シェーダーキャッシュ）
- レジストリクリーナー
- スタートアップマネージャー（各プログラムのブート影響を表示）
- ディスクアナライザー（インタラクティブなツリーマップ）
- デブローター（Windowsの不要ソフトウェア排除）
- プログラムアンインストーラー（残骸も削除）
- マルウェアスキャナー（シグネチャマッチング・ヒューリスティック分析・Windows Defender統合）
- プライバシーシールド（テレメトリ・広告ID・Cortana等30以上の設定を一括切替）
- セキュア削除（ランダムデータで上書きしてから削除）
- リアルタイムパフォーマンスモニター（CPU/メモリ/ディスク/ネットワーク/S.M.A.R.T.）
- クリーン前の1クリック復元ポイント作成、スケジュールスキャン、CLIモード、30言語対応

クリーニングルールはプレーンテキストのJSONファイルで管理されており、対応アプリを自分で追加できる。

## リポジトリ・ダウンロード

<https://github.com/AdventDevInc/kudu>

## Windows 11での導入手順

1. <https://github.com/AdventDevInc/kudu/releases/latest> を開く
2. 「Assets」から`Kudu-Setup-<バージョン>.exe`をダウンロード
3. 署名なし実行ファイルのためSmartScreen警告が出た場合は発行元がAdventDevIncであることを確認の上「詳細情報」→「実行」
4. インストーラーを実行（`%LOCALAPPDATA%\Programs\kudu`にインストールされ自動起動）
5. 左メニューに「System Cleaner」「Registry Cleaner」「Disk Analyzer」等が表示されれば導入成功

CLIモードは[CLI.md](https://github.com/AdventDevInc/kudu/blob/main/CLI.md)参照。

## 注意事項

レジストリクリーナーやシステムファイル削除機能を含むため、実行前にシステムの復元ポイント作成（アプリ内「System Restore Points」機能）を推奨。削除対象は必ず確認してから実行すること。各リリースのVirusTotalスキャン結果がリリースノートに記載されているため、実行前にウイルスチェックを行うこと。
