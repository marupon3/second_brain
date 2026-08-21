---
title: セッション作業アーカイブ
updated: 2026-08-21
---

# セッション作業アーカイブ

過去セッションで「何をしたか」の時系列記録（エピソード記憶）。**セッション開始時に読む必要はない**。特定の経緯を遡って確認したいときだけ参照する。

現在進行中の未解決事項は[[session-handoff|セッション引き継ぎメモ]]、いつ学んだかに依存しない知識は[[第二の脳の運用ナレッジ]]にある。Skills（`/ingest`等）の実行記録は`wiki/log.md`。

## 完了した作業（古い順）

1. **フォルダ再構成**: `raw/` `daily/` `projects/` `areas/` `resources/` `templates/` を `obsidian_vault/` 配下に集約。`wiki/` `weekly/` はリポジトリ直下のまま。
2. **`obsidian_vault/private/`追加**: パスワード等の非公開ノート用ローカル専用フォルダ（`.gitignore`除外）。
3. **venv誤コミットの削除**、`.venv`を作らない運用ルールをREADME.mdに明記。
4. **`obsidian-claude-guide.html`の文字化けバグ修正**（`<!DOCTYPE html>`等の欠落が原因）。
5. **ブランチ運用の整理**: `main`に進んでいた作業を`claude/sync-local-to-github-zyskxk`に統合。
6. **大規模`/ingest`実施（ローカルセッションにて）**: `obsidian_vault/raw/`配下の約460〜470件を全件処理し、`wiki/`に大量のページを生成・追記（詳細は`wiki/log.md`参照）。処理中、`apple_memo/`（OneNoteエクスポート由来）に個人の認証情報が多数含まれていたため、ファイル単位で判定し`private/`移動または`.gitignore`除外で対処済み。
7. **セキュリティインシデント対応（完了）**: `raw/pdfs/`配下の画像に**有効なGoogle APIキーが平文で写り込み、既にGitHubへpush済み**であることが発覚。
   - リポジトリの公開範囲を確認 → **Private確認済み**（第三者への公開はなし）
   - ユーザーがGoogle Cloud ConsoleでAPIキーを**即座に失効・再作成済み**
   - 該当画像ファイルを現在のツリーから削除・push済み（コミット`97d3c61`）
   - **未対応**: 過去のコミット履歴（`89989b9`）には画像がまだ残っている。完全に消すには`git filter-repo`等での履歴書き換え＋force pushが必要（緊急度低、Private repoのため）
   - 同様に`apple_memo/`内で発見されたAnthropic APIキー・GitHubトークン等は、該当フォルダが`.gitignore`済みのため未コミット＝リポジトリへの漏洩なし（ユーザーには失効推奨を伝達済み、対応状況未確認）
8. **`wiki/log.md`のマージコンフリクト解決**: ローカルとリモート双方からの追記が競合し、一度はコンフリクトマーカーが残ったままコミット・pushされてしまうミスがあったが、修正・再push済み。
9. **`obsidian_vault/raw/`の大量削除の切り分け**: `daily/`5件の削除は**意図的**と確認、コミット済み。その他`raw/`配下の削除は既存wikiへの要約が完了済みのため安全と判断しコミット済み。
10. **`remotely-save`同期プラグインを無効化**: 繰り返し発生していた`raw/`ファイルの原因不明の消失の根本原因の疑いがあったため、ユーザーがObsidian上で無効化。
11. **`Clippings/`フォルダの扱い**: Chrome拡張「Obsidian Web Clipper」の保存先。`raw/Clippings/`への移動方法と、拡張機能側のフォルダ設定変更手順を案内。移動作業中に発生した「Vault not found」エラーは拡張機能のVault名設定不備が原因と診断 → **ユーザーが解決済みと報告**。
12. **保留事項3件をリポジトリ調査で切り分け**（コード変更なし・調査のみ）:
    - Vaultルート問題: `.obsidian/`の実位置と`daily-notes.json`の相対パス設定から、Vaultルートが`obsidian_vault/`であることを確定。
    - `WEBから`重複疑い: `wiki/log.md`に既に処理済みの記録（バッチ22・23）を発見し、追加対応不要と判明。
    - `remotely-save`無効化の経過観察: 設定ファイル上で無効化されていることを再確認。新規の消失なし。
13. **`obsidian_vault/`構造図の作成**: フォルダ構成をSVGツリー図にまとめ、Artifactとして公開。`wiki/`・`weekly/`がVault外にある問題を視覚的に示した。
14. **`areas/`・`resources/`・`projects/`の廃止**: 未使用の補助整理フォルダを削除し、関連ドキュメント（`CLAUDE.md`・`README.md`・`obsidian-claude-guide.html`・`scripts/setup.py`）から参照を除去。当初は`wiki/`・`weekly/`も削除対象に含まれていたが、確認質問の結果ユーザーが「それらは維持、`areas/`・`resources/`のみ削除」と回答したためスコープを修正した。
15. **`raw/`自動リンク機能の検討・導入開始**: Smart ConnectionsとPython自作の2案を提示し、ユーザーがSmart Connections採用を選択。`.gitignore`に埋め込みキャッシュの除外設定を追加し、プラグインのインストール・設定手順を案内（除外フォルダ設定・動作確認は持ち越し）。
16. **Vaultルート不一致の解消（2026-08-18）**: (a)`wiki/`・`weekly/`を`obsidian_vault/`配下へ移動 (b)Vaultをリポジトリ直下に付け替え (c)現状維持＋ドキュメント修正、の3案を提示 → **ユーザーが(c)を選択**。`CLAUDE.md`2節・`README.md`のVault構造説明を実態に合わせて修正。ファイル移動は行っていない。
17. **グラフ・記憶アーキテクチャの導入検討（2026-08-18）**: 外部リポジトリ（claude-obsidian）、LangGraph等のワークフローグラフ、Memory Engineeringの3件について導入可否を調査。前2者は過剰設計として見送り、Memory Engineeringは既存の記憶機構の是正として一部採用（判断根拠は[[第二の脳の運用ナレッジ]]）。
18. **`scripts/`のリファクタリングと文字化け対策（2026-08-18）**: 4スクリプトの共通処理を`scripts/cli_common.py`へ集約し、長大関数を分割（挙動不変をゴールデンベースライン比較で検証）。全スクリプトで標準出力・標準エラーのUTF-8設定を行い、読み込みを`utf-8-sig`に変更してBOM混入を解消。`.claude/skills/research/`を定義名に合わせ`query/`へリネーム。`docs/operation-manual.md`を削除し実用部分を`README.md`へ統合、存在しない設計書への参照14箇所を除去。
19. **`/lint`へOKM freshness policy導入（2026-08-21）**: 変動する事実（件数・進捗・設定有無等）の書き方を「時点の記録／ポインタ／日付コンテナへの退避」の3形式に整理し、`CLAUDE.md`6.3節に明文化。`/lint`に検出基準5（日付スタンプの無い変動する事実）・6（日付スタンプの鮮度切れ、30日超）を追加。引用例外用に`<!-- freshness: example -->`抑制コメントを導入。
20. **`raw/pdfs/` → `raw/figures/` 名称統一（2026-08-21）**: フォルダ名を実態（画像ファイル中心）に合わせて`figures/`へ統一。`CLAUDE.md`・各Skill定義（`ingest`等）内の参照箇所を修正。
21. **ブランチ整理とsession-handoff.mdのgit検知トラブル解消（2026-08-21）**: リモートセッション側で作業していた`claude/smart-connections-vault-root-padj3n`と、ユーザーのローカルPCが実際にpushしていた`claude/sync-local-to-github-zyskxk`の2ブランチが並行していたことが判明。コミット履歴を比較し、後者が最新かつユーザーの実作業ブランチと確認。前者の変更（OKM導入・パス統一）を後者へマージ（コミット`db1278d`）し、以後は`claude/sync-local-to-github-zyskxk`に一本化。`session-handoff.md`の`作業ブランチ`記載もこれに合わせて修正。
22. **Smart Connectionsの設定完了確認（2026-08-21、完了）**: ユーザー環境に未インストールだったSmart Connectionsをインストール・有効化。「Manage excluded folders」で`private/**`・`_debug_remotely_save/**`・`daily/**`・`templates/**`を除外設定済み（`.obsidian/`はMarkdownを含まないため除外リストの選択肢に出現せず、対応不要と判断）。Reset data実行後、`raw/notes/生成AI/`配下のノートで動作確認 → 関連ノートパネルに類似度スコア付きで関連ノートが正しく表示され、**正常動作を確認**。ただし`daily/**`が除外対象のため、Daily Note自体を開いた場合は関連ノートパネルが機能しない可能性が残る（未検証）。

関連: [[session-handoff|セッション引き継ぎメモ]]、[[第二の脳の運用ナレッジ]]
