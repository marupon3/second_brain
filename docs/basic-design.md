# second_brain 基本設計書

要件は[[requirements|要件定義書]]を参照。本書は要件を満たすための構造・処理フロー・実装方針を定義する。

## 1. 全体構成

```
second_brain/
├── .claude/
│   ├── hooks/          # PreToolUse Hooks（機構的な安全機構）
│   │   ├── block-dangerous-git.sh
│   │   ├── block-raw-bash.sh
│   │   ├── block-raw-edit.sh
│   │   └── block-secret-write.sh
│   ├── settings.json    # Hook登録・permissions設定
│   └── skills/           # daily / ingest / lint / query / weekly
├── docs/                  # 要件定義書・基本設計書（本書）
├── obsidian_vault/        # ObsidianアプリのVaultルート
│   ├── .obsidian/
│   ├── daily/              # 日次ノート（人間+AI）
│   ├── private/             # 非公開情報（人間のみ、.gitignore対象）
│   ├── raw/                  # 不変ソース（人間のみ）
│   │   ├── articles/
│   │   ├── notes/
│   │   ├── figures/
│   │   └── personal/
│   └── templates/            # 固定テンプレート
├── scripts/                # 環境チェック・セットアップ用ユーティリティ
├── weekly/                 # 週次レビュー（AI生成、Vault外）
├── wiki/                   # AI生成知識ベース（Vault外）
├── .env / .env.example
├── CLAUDE.md               # AI運用マニュアル
├── pyproject.toml
└── README.md
```

`obsidian_vault/`がObsidianアプリのVaultルートであり、`.obsidian/`設定フォルダの実位置がその根拠となる。`wiki/`・`weekly/`はVault外に置くAI運用専用ディレクトリであり、Obsidianアプリからは見えずwikilinkも解決されない。この構成は意図的な現状維持であり、詳細は[[第二の脳の運用ナレッジ]]の確定事項を参照。

## 2. フォルダ責務設計

| フォルダ | 管理者 | 役割 | 更新契機 |
|---|---|---|---|
| `obsidian_vault/raw/` | 人間のみ | 不変の原文・スクラップ | 人間が随時投入 |
| `wiki/` | AI | `raw/`から生成した要約・概念・エンティティページ | `/ingest`実行時 |
| `obsidian_vault/daily/` | 人間+AI | 日次ノート（人間メモ/AI生成/タスクの3セクション分離） | `/daily`実行時 |
| `weekly/` | AI | 週次レビュー | `/weekly`実行時 |
| `obsidian_vault/private/` | 人間のみ | 非公開情報。`.gitignore`除外、AIのRead自体もHookで拒否 | 人間が随時編集 |
| `obsidian_vault/templates/` | 人間+AI | Daily Note等の固定テンプレート | 必要時 |
| `docs/` | 人間+AI | 要件定義書・基本設計書 | 仕様変更時 |

セクション分離設計（`daily/`）と管理者分離設計（`raw/` vs `wiki/`）により、「人間が書いた一次情報」と「AIが生成した二次情報」を常に区別できる状態を保つ。これがraw/への書き込み禁止（4節）の設計上の根拠となる。

## 3. Skills設計

全Skillsは`.claude/skills/<名前>/SKILL.md`に定義し、Claude Code CLI上の手動コマンド実行のみをトリガーとする（スケジュール実行なし）。

### 3.1 `/ingest`（データ取り込み・構造化）

```
raw/の未処理ファイル検出
  → 20件超か？
      Yes: ファイル単位でサブエージェントに分担
             → 各サブエージェントがwikiページを生成（index.md/log.mdへの書き込みは禁止）
             → オーケストレーターが集約し、index.md・log.mdを1回で更新
      No:  順次処理（読解 → 要約・構造化 → wiki生成/更新 → index.md・log.md更新）
```

- **設計意図**: 並列化時にサブエージェントへ索引・ログの書き込みを許すと、複数エージェントの同時書き込みで追記が競合する（後勝ちで内容欠落）。そのため書き込み権限をオーケストレーターに一本化した。
- PDFはテキスト抽出のみを構造化対象とし、画像・図表本体の保持は非対応（スコープ外、要件定義書6節）。
- 変動する事実は日付スタンプ（原文の観測日を優先）またはポインタで記述する（6.3節の运用と同一ルール）。

### 3.2 `/daily`（日次ノート）

```
当日ノートは存在するか？
  No:  templates/daily-note.mdから新規作成
  Yes: 既存内容を読み込んでから更新
        → 「人間メモ」セクションは変更しない
        → 「AI生成」「タスク」セクションのみ追記・更新（同一セクション内は後勝ち）
```

人間編集セクションの不可侵性は、機構的強制（Hook）ではなくSkillの手順記述による運用ルールであり、`raw/`と異なりHookでの強制対象にはしていない（判断を要する範囲のため。設計判断は5.2節参照）。

### 3.3 `/weekly`（週次レビュー）

直近7日分の`daily/`ノートを読み取り専用で収集し、完了・未完了タスクとAI生成セクションの主要トピックを要約して`weekly/YYYY-Www.md`（ISO週番号）に出力する。`daily/`・`raw/`はいずれも編集しない。

### 3.4 `/lint`（整合性・鮮度検査）

検出のみを行い、修正は行わない設計（4節の禁止事項に対応）。検出基準は6種類:

1. `updated:`の形式・鮮度（90日超で棚卸し候補）
2. 実在しないパスへの参照（廃止済みフォルダ名`areas/` `resources/` `projects/` `docs/`の残存を含む）
3. `source:`原文の消失
4. 同一事実の重複記載
5. 日付スタンプの無い変動する事実
6. 日付スタンプの鮮度切れ（30日超）

基準5・6は「事実の3形式」（不変の事実／時点の記録／ポインタ）というOKM（Operational Knowledge Model）freshness policyに基づく。日付が前提となる場所（`log.md` `session-archive.md` `daily/` `weekly/`）は検査対象外とし、誤検知を避ける。判定は機械的断定を避け候補提示に留め、報告時は「再観測／ポインタ化／退避」の3択をユーザーに提示する。

### 3.5 `/query`（質問応答）

`wiki/`を中心に`daily/` `weekly/`も含めファイルシステムを直接走査する（インデックスなし設計）。回答は参照元をwikilinkで明示し、保存はユーザー了承時のみ行う。大規模Vault（千ページ超）ではフォルダ・タグでの絞り込みを推奨する。

## 4. 記憶の階層設計

`wiki/`配下は記録の性質で置き場所を分離し、セッション開始時に読むページを`session-handoff.md`のみに限定する設計とする。

| ページ | 性質 | 読むタイミング |
|---|---|---|
| `session-handoff.md` | 作業中記憶 | 毎セッション開始時 |
| `第二の脳の運用ナレッジ.md` | 意味記憶 | 必要時（wikilink経由） |
| `session-archive.md` | エピソード記憶 | 経緯を遡る必要がある時のみ |
| `log.md` | 実行記録 | Skills実行結果の確認時 |

削除は「対象特定（`git grep`）→ 派生記述の洗い出し → ユーザー承認 → 削除実行 → 必要なら経緯をアーカイブへ記録 → index.mdからのリンク除去」という手順で行う。取り消し線等で本文に痕跡を残さないのは、履歴の正をGitコミットに一本化する設計判断による（Vault内に二重の履歴を持たせない）。

## 5. セキュリティ設計

### 5.1 Hookアーキテクチャ

`.claude/settings.json`のPreToolUse Hookとして、Bash/Edit/Write/NotebookEditの各ツール呼び出し前に検証スクリプトを実行する。

```
ツール呼び出し
  → PreToolUse Hook（matcherでツール種別を判定）
      → .claude/hooks/*.sh を実行（jqが無いWindows環境のためPython3でJSON入出力）
          → 危険パターンに一致 → ブロック（exit code / JSON出力でdeny）
          → 一致しない → 許可
```

| Hook | 対象イベント | 検証ロジック |
|---|---|---|
| `block-raw-edit.sh` | Edit/Write/NotebookEdit | 書き込み先パスが`obsidian_vault/raw/`配下かを判定 |
| `block-raw-bash.sh` | Bash | コマンド中の対象パスが`raw/`配下、かつ`rm`/`mv`/`sed -i`等の破壊的コマンドかを判定 |
| `block-secret-write.sh` | Edit/Write/NotebookEdit | 書き込み内容にGoogle(`AIza`)/Anthropic(`sk-ant-`)/GitHub(`gh[pousr]_`)/AWS(`AKIA`)/OpenAI(`sk-`)形式のパターンが含まれるかを判定 |
| `block-dangerous-git.sh` | Bash | `shlex`でコマンドをトークン化し、パイプ・演算子で区切った各セグメントに`push --force`・`reset --hard`・`clean -f`系・`checkout/restore .`・`branch -D`が含まれるかを対象パス問わず判定 |

`obsidian_vault/private/**`への読み取りはHookではなく`.claude/settings.json`の`permissions.deny`で拒否する（ツール呼び出し自体が発生しないPreToolUseより手前の層）。

### 5.2 強制範囲の設計判断

CLAUDE.mdの禁止事項のうち、Hookで機構的に強制する対象は「取り返しのつかない事故になり得るもの」に限定した。

- **Hookで強制**: `raw/`編集・秘密情報書き込み・破壊的Gitコマンド・`private/`読み取り。いずれも一度発生すると復旧困難、または実害（情報漏洩）に直結する。
- **ガイダンスに留める**: `private/`内容の`wiki/`への転記禁止、`/lint`結果の無断自動修正禁止。出力内容の妥当性判断を要するため機械的パターンマッチでは判定できず、誤検知でSkillsの正当な処理を止めるリスクがHookのメリットを上回ると判断した。

Hookは検知パターン一致時のみブロックする設計とし、誤検知の可能性がゼロでないことを前提に、ブロック時はユーザー確認または代替手段の検討を促す。

## 6. データフロー概観

```
[人間] raw/へ投入
   ↓
/ingest → wiki/へ構造化（index.md, log.md更新）
   ↓                              ↑
[人間+AI] daily/ ← /daily        参照
   ↓
/weekly → weekly/へ集約
   ↓
/lint → 整合性・鮮度レポート（wiki/log.md, wiki/lint-report.md）
   ↓
[人間] レポートを見て手動修正 or 個別に修正指示
```

`/query`は上記のいずれの生成物（`wiki/` `daily/` `weekly/`）も横断的に参照し、フローに書き込みを発生させない読み取り専用の経路として独立する。

## 7. 実装上の制約・前提

- 全スクリプト・Hookは対象環境（Windows 11 / Python 3.11.9）で動作すること。`jq`が無い前提でHookはPython3でJSON入出力を行う。
- ファイル入出力は常にUTF-8を明示する（BOM混入対策として読み込みは`utf-8-sig`を使用）。
- `scripts/`配下の共通処理は`scripts/cli_common.py`に集約し、重複を避ける。
- 仮想環境フォルダ名は`venv`固定（`.venv`は作成しない）。`uv`は`UV_PROJECT_ENVIRONMENT`で`venv`を明示指定する。

## 8. スコープ外・today's non-goals

要件定義書6節と同一。加えて、本書時点でインデックス構造（検索用DB等）は設計対象外とし、`wiki/`はファイルシステム走査のみで運用する（性能目安は要件定義書5.4節）。

## 9. 関連ドキュメント

- 要件は[[requirements|要件定義書]]を参照。
- Vault構造の確定事項・検討経緯は[[第二の脳の運用ナレッジ]]・[[session-archive|セッション作業アーカイブ]]を参照。
- ディレクトリ構成の可視化は[[second-brain-vault構成]]を参照。
