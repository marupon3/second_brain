---
title: SharePoint運用Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Tips/2026-06-16 SharePointでのファイル管理.md
  - obsidian_vault/raw/notes/Tips/2026-07-27 _SharePointで日程調整.md
  - obsidian_vault/raw/notes/生成AI/2025-01-16 リストの同期.md
---

# SharePoint運用Tips

## SharePointでの日程調整

参考記事: <https://note.com/echigoya_note/n/n47a84d42d249>

## Power AutomateでSharePointリスト同士を同期する

Aリスト（同期元）で発生した作成・更新・削除をBリスト（同期先）に反映させるフローを、3種類のトリガーで構築する例。

1. **アイテム作成時**: トリガー「SharePoint - アイテムが作成されたとき」（Aリスト）→ アクション「SharePoint - アイテムを作成」（Bリスト、動的コンテンツで列をマッピング）
2. **アイテム変更時**: トリガー「アイテムが変更されたとき」（Aリスト）→「アイテムの取得」でBリスト内の対応アイテムを検索（OData クエリで絞り込み可）→ 条件分岐で存在すれば「アイテムを更新」、なければ「アイテムを作成」
3. **アイテム削除時**: トリガー「アイテムが削除されたとき」（Aリスト）→「アイテムの削除」（Bリスト）。削除トリガーでIDが取得できない場合は、Aリスト側にBリストのアイテムIDを保持しておくなどの工夫が必要

**注意点**: AリストとBリストの列構造を揃えておく、ID管理（相互のアイテムIDを保持）、列名変更・追加時はフローのマッピングも修正、更新頻度が高いリストではトリガー条件式で処理を最適化する。

## 関連

- [[git-Tips|Gitコマンド Tips]]
