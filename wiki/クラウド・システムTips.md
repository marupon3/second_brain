---
title: クラウド・システムTips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Tips/2026-02-14 _Google_Cloud登録.md
  - obsidian_vault/raw/notes/Tips/2026-03-11 _WinPE起動.md
  - obsidian_vault/raw/notes/生成AI/2026-03-26 _gws drive操作.md
---

# クラウド・システムTips

## Google Cloud（Cloud Vision API）の有効化とサービスアカウント作成の流れ

1. Google Cloud Consoleで対象プロジェクトのCloud Vision APIを有効化する
2. 「IAMと管理」→「サービスアカウント」からサービスアカウントを作成
3. ロールは本来「Cloud Vision API ユーザー」が推奨だが、選択肢にない場合は「Editor」で代用可
4. 作成したサービスアカウントの「鍵」タブから「キーを追加」→「新しいキーを作成」→JSON形式を選択
5. ダウンロードされたJSONキーファイルを認証情報として利用する

原文にはプロジェクトID・請求先アカウントID・登録メールアドレス等の具体的なアカウント情報が含まれていたが、秘密情報のため本ページには転記していない。

## Windows: 次回起動時に確実にWinRE（回復環境）へ入る

```
:: 管理者権限のコマンドプロンプトで
reagentc /boottore
shutdown /r /t 0
```

再起動後、オプションの選択画面（続行／トラブルシューティング／PCの電源を切る）が表示される。

## gws（Google Workspace CLI）でのDrive操作

- ファイル一覧を見る: `gws drive files list`
- 特定ファイルを検索: キーワード指定で検索
- ファイルをエクスポート: PDF変換等の形式指定エクスポート
