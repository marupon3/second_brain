---
title: セッション作業アーカイブ
updated: 2026-08-26
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

23. **ローカルPC側の大量未コミットファイルの整理・`/ingest`実行（2026-08-21、完了）**: ローカルPCに長期間untrackedのまま溜まっていた`obsidian_vault/raw/`配下176件・Daily Note・`wiki/ループエンジニアリング.md`をpush（コミット`daffd20`）。origin側と並行して進んでいたセッション引き継ぎ整理とdivergedしていたため`git pull`でマージ（コンフリクトなし、`10e84cf`）。`raw/pdfs/`に新規作成されていた画像5件を`raw/figures/`へ統一（`2dc2147`）。続けて`/ingest`を実行し、サブエージェントで48件を過去処理済みの重複（フォルダ名リネーム・旧apple_memo再出現）と確認、真に新規だった7件（Claude隠れ機能25選・Loop/Graph責任分離・Context Engineering層・エージェントメモリ設計・セカンドブレインのコンパイラアーキテクチャ・テキスト抽出プロンプト）をwikiへ反映した（`181b52c`）。検証の過程で、`wiki/log.md`が「反映済み」と記録していたのに実際のwikiページには存在しない記述（[[グラフエンジニアリング]]の実践5ステップ節、[[ライフハック・自己啓発メモ]]のリーダーとマネジャー、[[日経ビジネス記事メモ]]のトークンエコノミー）を発見・復元し、[[各種ツールメモ]]のfrontmatterに残っていたGitマージコンフリクトマーカーも解消した。

24. **`.claude/hooks/`によるHook保護の拡充（2026-08-22、完了）**: 外部記事（CLAUDE.md設計指針・GitHub自動化ツールまとめ・Claudeスキル集）を材料に改善余地を検討する過程で、3件のHook/permissions強化を行った。
    - `obsidian_vault/private/`の読み取りを`.claude/settings.json`の`permissions.deny`で拒否（`bb2df91`）。従来`.gitignore`によるコミット除外はあったが、Claude Codeによる読み取り自体を止める設定は無かった。
    - `block-secret-write.sh`を追加（`0a7923a`）: Edit/Write/NotebookEditで書き込まれる内容にGoogle/Anthropic/GitHub/AWS/OpenAI形式のAPIキーらしきパターンを検知した場合にブロック。過去に`raw/`内の画像へGoogle APIキーが写り込みpush済みだった実インシデント（アーカイブ7参照）を踏まえた対応。
    - `block-dangerous-git.sh`を追加: `git push --force`・`git reset --hard`・`git clean -f`系・`git checkout/restore .`・`git branch -D`を、対象パスを問わずリポジトリ全体でブロック。既存の`block-raw-bash.sh`は`obsidian_vault/raw/`を対象にした場合のみ破壊的コマンドをブロックする設計だったため、Git操作そのものを対象にした汎用的な保護を別Hookとして追加した。README.mdが既に案内していた「`git reset --hard`を使わず`git revert`で戻す」方針を機構的に裏付ける形になった。
    - いずれもjqがWindows環境に無いため既存Hookと同様python3でJSON入出力する実装とし、実際のツール呼び出し（Write/Bash）でブロックされることを確認済み。`CLAUDE.md`4.1節・README.md「Hookによる保護」に一覧表を追記し、Hookで機構的に強制している範囲を文書化した。

25. **`docs/`の要件定義書・基本設計書を新規作成（2026-08-25、完了）**: `docs/requirements.md`（機能要件7項目・非機能要件5項目）・`docs/basic-design.md`（フォルダ責務設計・Skills処理フロー・記憶階層設計・Hookアーキテクチャ・設計判断の根拠）を作成した。既存のCLAUDE.md・README.md・各SKILL.md・`.claude/hooks/`の実装内容を一次情報として整理したもので、新たな仕様追加ではない。旧`docs/operation-manual.md`（2026-08-18廃止、実用部分は`README.md`へ統合済み）とは別物。`README.md`の「基本設計書は本リポジトリには同梱していない」という記述が実態と食い違っていたため訂正し、`README.md`・`CLAUDE.md`のディレクトリ一覧・[[second-brain-vault構成|second_brainのディレクトリ構成]]に`docs/`を追加した。

26. **`/weekly`を未実行週バックフィル仕様に改訂（2026-08-26、完了）**: ユーザーから「`weekly/`に`2026-W32.md`はあるが`W33` `W34`が無い」という指摘を受け調査した結果、旧仕様が「実行日を含む週のみ」を処理する設計であり、`/weekly`を実行し忘れた週は後から実行しても永久に生成されないという設計上の欠陥と判明した。ユーザーと4回の質問応答（既存ファイル衝突時の挙動・追記方式の採否・バックフィル範囲・日付抽出ルール）を経て以下の設計に決定した。
    - 生成トリガーを「実行タイミング」から「`daily/`の実データの有無」へ転換。実行日を含むISO週から遡って直近N週（既定4週≒1ヶ月、実行時に指定変更可）を走査し、データがある未生成週をバックフィル生成する。無制限走査は将来`daily/`が大量になった際の性能リスクを避けるため採用しなかった。
    - `daily/`の実ファイルが`YYYY-MM-DD.md`形式ではなく外部同期ツール由来の命名（`2026-08-16 ClaudeObsidian Radar Daily Summary.md`等）だったため、ファイル名先頭が`YYYY-MM-DD`であれば日付とみなす抽出ルールを新設。
    - 既存`weekly/`ファイルとの衝突はoverwrite/skipをユーザーに都度確認する方式を採用（存在しない週は確認不要）。追記（append）方式は、`weekly-review.md`テンプレートが4セクション固定の単一文書であり同一セクション見出しが繰り返される構造になるため不採用と判断した。
    - `.claude/skills/weekly/SKILL.md`を全面改訂し、`CLAUDE.md`5節・`docs/requirements.md`4.4節・`docs/basic-design.md`3.3節に反映した。

関連: [[session-handoff|セッション引き継ぎメモ]]、[[第二の脳の運用ナレッジ]]
