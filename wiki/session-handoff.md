---
title: セッション引き継ぎメモ
updated: 2026-08-21
---

# セッション引き継ぎメモ

**次セッションが最初に読む唯一のページ。** ここには「今アクティブな未解決事項」と「毎回必要な前提」だけを置く。

| 置き場所 | 内容 | 読むタイミング |
|---|---|---|
| このページ | 未解決事項・次の一手・恒久的な制約 | **毎セッション冒頭** |
| [[第二の脳の運用ナレッジ]] | いつ学んだかに依存しない知識・確定した判断 | 必要になったとき |
| [[session-archive\|セッション作業アーカイブ]] | 過去に何をしたかの時系列記録 | 経緯を遡るときだけ |
| `wiki/log.md` | Skills（`/ingest`等）の実行記録 | 処理済み判定のときだけ |

## 次回セッション開始プロンプト（コピペ用）

> `wiki/session-handoff.md`を読み込み、未完了タスクの最優先項目（`raw/`配下200件超の未コミットファイルの整理・`/ingest`実行）から作業を再開してください。作業開始時は「作業開始宣言」として、どのタスクを何分で終えるかを簡潔に報告してから着手してください。

---

## 1. 未解決事項（優先順）

1. **【最優先】ローカルPC側の大量未コミットファイルの整理**
   - 状況: ユーザーのローカルPC（Windows）で`git status -s`を実行したところ、`obsidian_vault/daily/`のDaily Note 5件と、`obsidian_vault/raw/notes/`配下の200件超のノート（Claude Code・Python・PSQL・Linux・Windows・Tips等の既存サブフォルダ、および新規の`raw/clippings/`・`raw/notes/AI/`・`raw/notes/Library/`・`raw/notes/books/`・`raw/notes/drug/`）、`raw/figures/working_memory.jpg`、`raw/pdfs/`（旧フォルダ、要確認）、`wiki/ループエンジニアリング.md`がuntrackedのまま溜まっている。
   - 次のアクション:
     (a) `raw/pdfs/`がまだ存在する場合、前回セッションで`raw/figures/`へ統一済みのはずなので重複・残骸でないか確認する。
     (b) `obsidian_vault/raw/`配下の新規ファイル群に対して`/ingest`を実行し、`wiki/`への構造化ページ生成を行う。
     (c) `obsidian_vault/daily/`のDaily Note・`wiki/ループエンジニアリング.md`はraw以外なので、`/ingest`と別に内容を確認した上でgit commitする。
     (d) 作業前に必ず`git fetch`＋`git status`でリモートとの差分を確認すること（本セッション冒頭のルール）。

2. **Smart Connectionsの`daily/**`除外設定の見直し（任意）**
   - 状況: Smart Connectionsは2026-08-21にインストール・動作確認済み（`raw/notes/生成AI/`のノートで関連ノートパネルが正常表示）。ただし「Manage excluded folders」に`daily/**`が含まれているため、Daily Note自体を開いた場合に関連ノートパネルが機能するかは未検証。
   - 次のアクション: 必要であれば`daily/**`を除外リストから外し、Daily Noteでも関連ノート表示が機能するか確認する（優先度は低い。ユーザーの使い方次第で不要な場合もある）。

3. **`remotely-save`無効化後の経過観察（継続中）**
   - 状況: `obsidian_vault/.obsidian/community-plugins.json`上で無効化を確認済み。新規の原因不明な消失は今のところなし。
   - 次のアクション: `raw/`配下のファイル数・内容の変化を引き続き注視する。

4. **（緊急度低・任意）漏洩画像のgit履歴からの完全削除**
   - Google APIキーが写り込んだ画像がコミット`89989b9`に残存。キーは失効・再作成済み、リポジトリはPrivateのため緊急度は低い。完全削除には`git filter-repo`＋force pushが必要。

5. **（緊急度低・任意）`apple_memo/`内で発見されたAPIキーの失効確認**
   - Anthropic APIキー・GitHubトークンについて、ユーザーに失効を推奨済みだが対応状況は未確認。リポジトリへの漏洩はなし（`.gitignore`済み）。

## 2. 次にやること

- **タスク1**: ローカルPC側の未コミットファイル整理（上記1）。期待する出力は、`/ingest`によるwikiページ生成完了と、Daily Note等のコミット・push完了。

## 3. 制約と前提条件

- 言語: 日本語優先（プロンプト・ノート・ファイル名・コミットメッセージすべて）
- 環境: Windows 11 / Python 3.11.9 / UTF-8（`CLAUDE.md` 1節）
- 作業ブランチ: `claude/sync-local-to-github-zyskxk`（`origin`に追随済み）
- ローカル（Windows PC、`C:\Users\marupon\PycharmProjects\second_brain`）とリモートセッションの双方から同じブランチへpushする運用。**作業開始前に必ず`git fetch`＋`git status`で差分を確認すること**（過去に双方pushでコンフリクトが複数回発生）。
- `obsidian_vault/raw/`はAIが編集・削除してはならない（`CLAUDE.md` 4節、不変の原文ソース）
- 破壊的操作（削除・大規模書き換え）は実行前に必ずユーザーへ確認する（`CLAUDE.md` 4節・6節）

## 4. このページの運用規律

このページは放置すると肥大化し、毎セッション読む価値が薄まる（実際に5日で約3倍まで膨らんだ経緯がある）。以下を守る。

- **解決した項目は取り消し線で残さず削除する。** 経緯を残す必要があれば[[session-archive|セッション作業アーカイブ]]へ移す。
- **セッションの作業内容をここに書き足さない。** 完了した作業は[[session-archive|セッション作業アーカイブ]]、恒久的な知識は[[第二の脳の運用ナレッジ]]へ振り分ける。
- **目安として本文200行以内に収める。** 超えたら1〜3節を見直し、アクティブでない記述を移す。
