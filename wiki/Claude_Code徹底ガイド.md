---
title: Claude Code徹底ガイド
updated: 2026-08-26
source:
  - "obsidian_vault/raw/notes/claude Code/2026-08-20-25-Hidden Claude Features Most People Completely Miss.md"
  - obsidian_vault/raw/notes/生成AI/2026-02-08 Claude.md
  - obsidian_vault/raw/notes/生成AI/2026-03-25 _Claude Code用Skills.md
  - obsidian_vault/raw/notes/生成AI/2026-03-25 _global Skills更新.md
  - obsidian_vault/raw/notes/生成AI/2026-07-29 _Claude Codeを他社APIで利用する.md
  - obsidian_vault/raw/notes/生成AI/無題.md
  - obsidian_vault/raw/notes/生成AI/2026-07-22 Clade Code + NotebookLM.md
  - obsidian_vault/raw/notes/生成AI/2026-02-19 _Claude Code公式.md
  - obsidian_vault/raw/notes/生成AI/2026-07-11 _Claude Code逆引き.md
  - obsidian_vault/raw/notes/providerによる生成AI無料実行.md
  - obsidian_vault/raw/notes/10のClaude + Obsidianリポジトリ.md
  - "obsidian_vault/raw/notes/Claude Code/2026-04-30-Claude Skills 72選.md"
  - "obsidian_vault/raw/notes/Claude Code/2026-04-15-Claudeの力を引き出す67の必須スキル.md"
  - "obsidian_vault/raw/notes/Claude Code/2026-01-31-ClaudeのためのSkills構築の完全ガイド (非公式日本語訳版).md"
  - "obsidian_vault/raw/notes/Claude Code/2026-08-26-Skill一覧.md"
  - obsidian_vault/raw/notes/Graph enginering.md
  - "obsidian_vault/raw/notes/claude Code/2026-08-18 Grok 4.6をそのまま呼び出せるプラグイン.md"
  - obsidian_vault/raw/notes/2026-08-06-本当に効くCLAUDE.mdの書き方.md
  - "obsidian_vault/raw/notes/Claude Code/2026-06-30-CLAUDE.mdの設計.md"
  - obsidian_vault/raw/notes/2026-08-05-AGENTS.md例.md
  - "obsidian_vault/raw/notes/claude Code/2026-08-18-Memory Engineering.md"
  - "obsidian_vault/raw/notes/Claude Code/2026-08-19-AI利用料を約1／13に抑える手順書.md"
---

# Claude Code徹底ガイド

「Master Claude Code」（Aakash Gupta, v1.0 2026年1月）等のガイド記事・実体験メモをまとめたもの。

## Claude Codeの位置づけ

チャットツールではなく、ワークフロー全体で動く「OS層」に近い。フルなファイルシステムアクセス、アップロード上限なし、数時間単位のタスク実行、MCP経由で外部ツールと連携できる点が従来のチャットAIとの違い。

## 隠れた25のClaude機能（Chat・Projects・Artifacts・Skills/Cowork・Claude Code）

「多くの人はClaudeをチャットボックスとしてしか使わず、実際にワークフローとして機能させる設定を有効化していない」という指摘に基づく機能棚卸し。共通するポイントは、Claudeの本当のアップグレードは個別の裏技ではなく「永続性（persistence）」——記憶・指示・ファイル・スキル・再利用可能なワークフロー——にあるということ。

- **設定（Settings）でほとんど誰も開かない項目**: プロフィール/カスタム指示（全会話に効く常設ルール）、過去のチャット履歴からの記憶と横断検索、コード実行とファイル作成の有効化（Artifacts/Skills/ファイル操作の前提。無効だと多くの機能が動かない最頻出のつまずき）、Effort control（low〜max/extraで推論の深さを選ぶ。タスク難易度にモデルの労力を合わせる仕組み。本Vaultの各Skillのeffort目安と同じ発想）、スタイル（口調・フォーマットのプリセット）。
- **Projects（最も過小活用されているワークスペース）**: プロジェクトごとに永続する背景情報・専用の指示（そのプロジェクト限定のシステムプロンプト）・ナレッジファイル（毎回自動で読み込まれる参照文書）・大規模プロジェクトでのRAGモード（ファイルが増えても全部をコンテキストに詰め込まず関連部分だけ取得）・プロジェクト個別のメモリ層（個人チャットと交差汚染しない）。
- **アウトプット系機能**: Artifacts（コード・文書・可視化を別パネルで表示し、会話と切り離して反復編集できる）、バージョン管理（更新・過去バージョンへの復元）、共有リンク、選択式・ステップ式の構造化された対話（自由記述だけに頼らない）。
- **Skills・Cowork・自動化**: Skills（`.claude/skills/名前/SKILL.md`として保存される再利用可能なプレイブック。本Vaultの`/ingest`等がこれに該当）とチーム内共有、スケジュール/リモートのCowworkセッション（PCを閉じても実行が継続）、大きなタスクを複数サブエージェントに分割して並列実行、コネクタ（ファイル・メール・カレンダー等を連結して1指示で横断作業）。
- **Claude Codeのパワー機能**: CLAUDE.mdの階層（ユーザーレベル`~/.claude/CLAUDE.md`／プロジェクトレベル`.claude/CLAUDE.md`／ディレクトリレベル、より具体的な階層が優先される）、`/init` `/plan` `/compact` `/review`等の乱れたセッションを防ぐスラッシュコマンド、実装前に計画を提示させ承認を待つPlan Mode、危険な操作をブロックし工程を強制するHooksと権限ルール、うまくいった一式を再利用可能なワークフロー/エージェントチームとして保存する仕組み。

**早く効果が出る優先順位**: プロジェクト＋指示（同じ前提を毎回貼らない）／メモリ＋過去チャット検索／Artifactsで成果物化／Skillsで反復プロセスをコード化／コーディングではCLAUDE.md＋Plan Mode。よくある失敗は、プロジェクト分けをせず1つの雑多なチャットで済ませる、毎セッション同じ文脈を貼り直す、Settings→Capabilitiesを何も有効化せず「なぜ動かないのか」と困る、Plan Modeやレビュー・保存済みワークフローを使わず行き当たりばったりで走らせる、の4つ。

## MCP（Model Context Protocol）

ClaudeをGitHub、Sentry、Linear、GitLab、Notion、Slack、Jira、Perplexity、PostgreSQL、Gmail等の外部ツールに接続する開放標準（「AI版USB-C」と説明される）。追加例:

```
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

## 主要スラッシュコマンド

| コマンド | 内容 |
| --- | --- |
| `/help` | 利用可能なコマンド一覧を表示 |
| `/clear` | コンテキストをリセット（タスクの合間に使う） |
| `/compact` | 会話を圧縮しトークンを節約 |
| `/model` | Opus/Sonnet/Haikuを切替 |
| `/mcp` | MCPサーバーの接続状況を確認 |
| `/doctor` | インストールの問題を診断 |
| `/config` | 設定を開く |

`@filename`でファイル参照、`!`から始めるとシェルコマンドを直接実行、Ctrl+Vで画像貼り付け、Escを2回でチェックポイントに巻き戻し。

## Skills と CLAUDE.md

- **Skills**: `~/.claude/skills/`配下にタスク特化の再利用可能な指示パッケージを配置。関連時にClaudeが自動読み込み
- **CLAUDE.md**: プロジェクトの永続的なコンテキストを与えるMarkdownファイル。グローバル設定は`~/.claude/CLAUDE.md`、プロジェクト設定は`./CLAUDE.md`
- 組み込みSkills例: `docx`（Word文書）、`xlsx`（スプレッドシート）、`pptx`（プレゼン）、`pdf`（PDF処理）

### 導入したSkillsの例（2026年3月時点メモ）

| Skill | 用途 | 起動する指示例 |
| --- | --- | --- |
| superpowers | 出力品質の底上げ、新機能設計時の自動ブレスト | 「新機能Xを追加したい」 |
| planning-with-files | 計画→実装のワークフロー | - |
| gogcli / google-workspace-cli | Gmail・カレンダー・Drive操作 | 「今日の予定を確認して」 |
| frontend-design | UIデザイン品質向上 | - |
| understand-anything | コードベース理解 | `/understand` |
| trailofbits/skills | セキュリティ監査 | 「このコードのセキュリティを監査して」 |
| playwright-skill | ブラウザ自動化 | 「このページをテストして」 |
| mcp-excalidraw | 図解生成 | 「システム構成図を作って」 |
| claude-health | 設定診断 | - |

### グローバルSkillsの更新手順

GitHubで管理するanthropic-skillsリポジトリをシンボリックリンク経由で`~/.claude/skills/`に反映する運用。

```powershell
cd ~\.claude\repos\anthropic-skills
git pull
```

シンボリックリンクは`New-Item -ItemType SymbolicLink`で`~\.claude\repos\anthropic-skills\skills`配下の各フォルダを`~\.claude\skills\`にリンクして作成済みのため、`git pull`だけで全スキルに反映され再起動も不要。

## Skillsの作り方（構築ガイド）

Anthropic公式PDF「The Complete Guide to Building Skill for Claude」の非公式日本語訳要約。

- **基本構造**: 必須はSKILL.md（YAMLフロントマター＋Markdown指示）。任意で`scripts/`（実行コード）・`references/`（ドキュメント）・`assets/`（テンプレート等）を追加できる。
- **コアデザイン原則**: ①プログレッシブ・ディスクロージャー（3層構造でトークン節約）②コンポーザビリティ（他スキルと併用可能）③ポータビリティ（Claude.ai / Claude Code / APIで共通）。
- **計画・設計**: 2〜3の具体的ユースケースから始め、成功基準を定量・定性で定義する。YAMLフロントマターの`name`＋`description`が最重要（トリガー条件を明確に）。
- **効果的な記述法**: descriptionには「何をするか」＋「いつ使うか」＋具体的フレーズを含める。指示は具体的・実行可能にし、エラーハンドリングと例を追加。詳細は`references/`に分離する。
- **テストと反復**: トリガーテスト／機能テスト／パフォーマンス比較を実施。アンダー／オーバートリガーや実行不具合に応じて改善する。
- **配布方法**: 個人はフォルダをZIP化してClaude.aiにアップロードするかClaude Codeに配置、組織はワークスペース全体に展開可能。
- **トラブルシューティング**: アップロード失敗→SKILL.mdの命名とYAML形式を確認、トリガーされない→descriptionの具体性を強化、過剰トリガー→ネガティブトリガーやスコープ明確化、指示無視→簡潔化・重要事項の強調・スクリプトによる検証。

## Claude Skillsカタログ（分野別・実践的な導入候補）

海外で話題になった2つの記事（[polydao氏の67選（英語原文）](https://x.com/polydao/status/2044317956893471081)と、それを日本のビジネス現場向けに4カテゴリへ再構成し独自3パック+2スキルを加えたClaudeCode_UT氏の72選）から、重複を除いて実際に導入可能な具体的Skillを分野別に整理したもの。

| Skill | 説明 | 入手先 |
| --- | --- | --- |
| Skill Creator | 要件からSKILL.mdを生成・評価・改善する公式ツール | anthropics/skills |
| Write a Skill | Skillの書き方（構造・description・ファイル分割基準）を教える | mattpocock/skills |
| Find Skills | キーワードから公開マーケットプレイス（SkillsMP等）を検索 | skillsmp.com |
| Brainstorming | 9ステップの構造化プロセスでアイデアを設計書に仕上げる。承認まで実装しない | obra/superpowers |
| Grill Me | 計画の考慮漏れを1つずつ質問で潰すインタビュー形式 | mattpocock/skills |
| Write a PRD | 会話文脈から直接PRD（企画書）を生成 | mattpocock/skills |
| PRD to Plan / PRD to Issues | PRDをタスク単位の実行計画、または垂直スライス単位のGitHub Issueに変換 | mattpocock/skills, obra/superpowers |
| Design an Interface | 1モジュールに3〜5個の異なる設計案を並行生成 | mattpocock/skills |
| TDD | テストファースト・Red-Green-Refactorを強制 | mattpocock/skills |
| Triage Issue / QA | バグ調査→根本原因特定→修正計画のIssue化、機能のQAパス | mattpocock/skills |
| Systematic Debugging | 4フェーズの体系的デバッグ手法（3回失敗で設計見直し） | obra/superpowers |
| Superpowers | TDD・デバッグ・ブレインストーミング等20個のエンジニアリングSkillの集合 | obra/superpowers |
| Improve Codebase Architecture | 浅いモジュールを深いモジュールに変換する改善提案 | mattpocock/skills |
| Code Review | セキュリティ/性能/エラー処理/アーキテクチャの体系的レビュー | anthropics/skills, obra/superpowers |
| Git Guardrails / Setup Pre-Commit | 危険なgitコマンドのブロック、lint-staged等のフック自動構築 | mattpocock/skills |
| Frontend Design / Canvas Design / Theme Factory | 「AIっぽくないUI」生成、デザイン哲学の言語化→ビジュアル化、カラーパレット一括生成 | anthropics/skills |
| Doc Co-Authoring | 情報収集→ドラフト→「読者テスト」の3段階で共同執筆 | anthropics/skills |
| Edit Article | 文章を情報依存関係グラフとして分析し構造から編集 | mattpocock/skills |
| Obsidian Vault | Obsidianと連携して知識を蓄積・検索（wikilinks・Index Note） | mattpocock/skills（kepano氏の自動タグ付け派生版も参照） |
| PDF / DOCX / PPTX / XLSX | PDF読取・結合・分割・OCR、Word編集、スライド生成、Excel数式・再計算検証 | anthropics/skills |

**組み合わせパックの考え方**: 単体Skillより「企画壁打ち（Brainstorming→Grill Me→Write a PRD）」「ドキュメント一括処理（PDF+DOCX+XLSX）」「リサーチ→執筆（Doc Co-Authoring→Edit Article）」のように複数Skillを順番に呼び出すワークフローパックとして`SKILL.md`に組むと効果が大きい。

**導入の始め方**: いきなり多数入れず、①メタスキル（Skill Creator・Write a Skill・Find Skills）→②自分の業務で最も時間を使っている作業に合うSkill1つ→③使って直して育てる、の順で進める。非公式スキルはGitHub経由で誰でも公開できるため、導入前にSKILL.mdの中身を確認しセキュリティリスクを考慮する。

## プロンプティングのコツ

- **Be Specific**: 「このCSVをきれいにして」ではなく「B列が空の行を削除し、メールアドレスで重複排除して」のように具体的に
- **Give Examples First**: 出力形式が重要な場合は1〜2個の例を先に示す
- **Chain Steps**: 複雑なタスクは「まず分析、次に要約、それから行動項目を作成」のように手順を連結
- **Set Constraints**: 「500語以内」「2024年のデータのみ使用」等の品質制約を設定
- **Assign Roles**: 「データアナリストとしてこのデータセットをレビューして」等、必要な専門性を割り当てる
- **`/clear`を頻繁に使う**: 関係のないタスクの間でコンテキストをリセットする

## CLAUDE.mdの最適化でミス率が劇的に改善する（実測データ）

30コードベース・6週間の検証で、CLAUDE.mdのルール設計によりClaudeのミス率が大きく改善したという報告。

| ルールセット | ミス率 |
| --- | --- |
| ルールなし | 41% |
| Karpathyの4ルール | 11% |
| 12ルール版 | 3% |

**最初の4ルール**（防ぐもの）:

1. 前提を明示する（勝手な思い込みを防ぐ）
2. 最小構成で解く（不要な抽象化を防ぐ）
3. 関係ないコードを触らない（無関係な修正を防ぐ）
4. 成功条件を決めて検証する（未検証の完了を防ぐ）

**追加された8ルール**（Claude Codeが複数ファイル・長時間タスク・Hooks/Skills/MCPを扱う「業務エージェント」に近づいたため）:

1. 判断だけAIに任せる（決定論的処理はコードに書く）
2. トークン予算を決める
3. 矛盾する実装を混ぜない
4. 書く前に周辺コードを読む
5. テストは「意図」まで検証する
6. 長い作業はチェックポイントを刻む
7. 不確実な成功は表面化させる

**結論**: CLAUDE.mdは「お願いリスト」ではなく、AIエージェントの行動契約書。毎回プロンプトで頑張るより、守るべきルールを明文化した方が出力が安定する。

## 本当に効くCLAUDE.mdの書き方（Anthropicエンジニアの流儀）

CLAUDE.mdはClaude Codeが毎回のセッション開始時に必ず読むファイル。長さが最も重要で、Anthropic公式でも**200行以下**（理想は60行前後）を推奨。300行を超えると信号が薄れて無視されやすくなる。

**よくある失敗パターン**:
- 空ファイル: 機会損失。毎回ゼロから推測させる。
- 肥大化: 数百行のドキュメント。Claudeは「ざっと見る」だけで吸収しない。

**成功の原則**:
- 普遍的に適用できる指示だけを入れる（毎回のセッションで有用なもの）。「変更後は必ず型チェックを実行」はOK、「DBスキーマ作成時はこの命名規則」のような状況限定の指示はNG（インポート先に移す）。
- Anthropicの内部チームは「記憶のない優秀な新入社員へのオンボーディングメモ」として扱っている。

**推奨構造**: ①プロジェクト概要（2〜3文）②よく使うコマンド（build/test/lintなど）③譲れないコードスタイル④テストの期待値⑤絶対に勝手にやってはいけないこと（破壊的操作など）⑥状況限定の内容は`@path/to/file`でインポート。

**その他のポイント**:
- 重要度の高い指示には「IMPORTANT」や「YOU MUST」を使う（乱用すると効果が消える）
- Markdownで見出し＋箇条書きにしてスキャンしやすくする
- Progressive Disclosure: 根のファイルは短く、詳細は別ファイルに分離
- 定期的に監査して矛盾・古いルール・不要なものを削除する
- 実際のセッションで「本当に従っているか」を検証する

結論: 短くて一貫して守られるファイルの方が、長くてたまにしか読まれないファイルよりはるかに有効。

## コピペで使えるCLAUDE.mdテンプレート集（7つのメカニズム）

「2,000時間の試行錯誤」を経た設計指針。上記の「本当に効くCLAUDE.mdの書き方」と補完関係にある実践的なテンプレート集。

**指示を伝える7つの仕組み**: CLAUDE.md／`.claude/rules/`／Skills／Subagents／Hooks／Output Styles／System Prompt。CLAUDE.mdはこのうち1つに過ぎず、「ガイダンス」であって「命令」ではない（100%守らせたいならHooksが必要）。全部をCLAUDE.mdに詰め込むと本当に大事なルールがノイズに埋もれる。

**CLAUDE.mdが無視される3つの原因**: ①ファイルが長すぎる（200行超で無視確率が上がる）②表現が曖昧（「きれいなコードを」ではなく「2スペースインデント、セミコロンなし」まで具体化）③CLAUDE.mdの役割の誤解（お願いレベルのガイダンスであり強制ではない）。`/init`で自動生成した内容はそのまま使わず「一度捨てるべき下書き」として扱う。

**設計思想「削るほど強くなる」**: 各行について「この行を削除したらClaudeは間違いを犯すか？」と自問し、Noなら削る。最適値はコミュニティ調査で60行前後、Anthropic公式は200行以下を推奨。

| メカニズム | ロードタイミング | コスト | 向いている用途 |
| --- | --- | --- | --- |
| CLAUDE.md | 常時ロード | 高 | ビルドコマンド・ディレクトリ構成 |
| `.claude/rules/` | パスマッチで発動 | 中 | ファイル固有の制約 |
| Skills | 名前だけ常時表示、本体はオンデマンド | 低 | 手順書・チェックリスト |
| Subagents | 呼び出し時のみロード | 低 | コード検索・レビュー |
| Hooks | イベント駆動 | — | Lint強制・危険コマンドのブロック（100%強制） |
| Output Styles | セッション開始時 | — | ロール変更 |
| System Prompt追加 | CLI起動時のみ | — | トーン・フォーマット指定 |

判断基準: 「100%守らせたい」→Hooks、「特定パスのファイル操作時だけ」→`.claude/rules/`、「30行以上の手順書」→Skills、「毎セッション必要」→CLAUDE.md。

**テンプレート4種**: ①グローバルCLAUDE.md（`~/.claude/CLAUDE.md`、作業スタイルと安全ルールのみ）②プロジェクトCLAUDE.md（60行程度、概要/ディレクトリ構成/開発コマンド/絶対ルール/ハマりポイント/Off-Limitsの6セクション）③`.claude/rules/`（YAMLフロントマターの`paths:`でファイルパターンごとに条件付き発動）④Hooks（危険コマンドのブロック・自動フォーマット・コミット前Lintゲートを`PreToolUse`/`PostToolUse`/`Stop`イベントのJSON設定で実装）。

## プロンプトキャッシュでAI利用料を抑える（約1/13の手順書）

Anthropic公式が無料公開したコスト最適化手順の要点。核心は「同じ前置き（system prompt＋ツール定義＋固定コンテキスト）を毎回送り直さずキャッシュ再利用する」こと——これが最も効果が大きく、1件あたりの料金がほぼ半分以下になる。

**基本の仕組み**: 前置きは先頭から順番に一致しないとキャッシュが効かない。「静的なものを先に、動的なものを後ろに」配置するのが鉄則（推奨順: ①静的システムプロンプト②ツール定義③CLAUDE.md等のプロジェクト知識④セッション共通コンテキスト⑤会話履歴）。日時等の動的な値をシステムプロンプトに埋め込むとキャッシュが毎回壊れるため、userメッセージ側に渡す。

**CLAUDE.mdのキャッシュ最適化**: CLAUDE.mdはプロジェクトコンテキスト層としてキャッシュされ、同じ内容が続く限り2回目以降は約1/10の料金。短く・信号密度高く（200行以下、理想60〜100行）・静的な内容だけ書く（日時やUUIDを入れない）・よく使うコマンドを具体的に書く・ワークフロー固有のものはSkillsに逃がす、が最大化のコツ。セッション中の編集はすぐには反映されず`/clear`や`/compact`まで古い版が使われ続ける点に注意。

**CLAUDE.mdとSkillsの役割分担**: CLAUDE.mdは「常に知っているべき事実・ルール」（セッション開始時に毎回全量ロード）、Skillsは「必要なときだけ使う手順・知識」（名前＋説明だけ常時、本体は必要時のみ）。「CLAUDE.mdの中に手順っぽい長いセクションが増えてきたら、それはSkillsに移すサイン」。

## AGENTS.md（AI実装原則の記述例）

CLAUDE.mdと並んで使われる、AIエージェントにソフトウェアを健全に成長させるための原則をまとめたファイルの例。

- 後方互換性を維持しない。互換性レイヤー・フォールバック・移行処理を追加するのではなく、古い経路は削除する。
- 現在の要件を完全に満たす、最も単純な実装を選ぶ。推測的な抽象化・設定項目・間接化は避ける。
- システムは層を重ねて成長させる。端から端まで動作する最小のバージョンから始め、すでに動作する製品の上に新しい機能を追加していく。動作する製品を未完成の複雑さと引き換えにしない。
- コンポーネントはモジュール化し、関心事を明確に分離する。
- 全体の複雑さを減らしたり信頼性を向上させたりできる場合は、確立されていてよく保守されているライブラリを優先する。明確な理由がない限り、一般的な機能を再実装しない。
- 自前の実装を書いたり新しいパッケージを追加したりする前に、まず既存の依存関係に頼る。ライブラリに機能がないと決めつけず、ドキュメントや型情報を確認する。
- 長期的な視点でアーキテクチャの決定を行う。今だけ動く応急処置で、後で置き換える前提のものを受け入れない。

## メモリエンジニアリング（AIエージェントの記憶設計）

「エージェントがタスクを終えた後、同じユーザーが戻ってきても何も覚えていない」問題を解決するための、記憶（Memory）設計の実践ガイド（@fleyta88の投稿より）。

**核心的な指摘**: これはプロンプトやモデルの問題ではなく「ストレージ（記憶の保存方法）」の問題。会話履歴を全部保存するのは「記憶」ではなく「トランスクリプト」に過ぎない。本当の記憶とは「その会話が終わった後も、将来必要になる事実」のこと。

**7ステップの要点**:
1. **保存するものを厳選する**: 「この情報は将来のターンで参照されるか？」と問う。決定事項は記憶、雑談や途中の選択肢は基本的に不要。
2. **取り出せなければ意味がない**: 保存した事実には「明確な主語」「安定した表現」「スコープ（誰の情報か）」の3つが必要。スコープを忘れると他人の情報が混ざる事故が起きる。
3. **記憶の形は主に3種類で十分**: Working memory（今のタスク中だけ＝コンテキストウィンドウ）、Episodic memory（何が起きたか）、Semantic memory（ユーザーの役割・好み・技術スタックなど永続的な事実）。ほとんどのシステムはWorkingだけで終わり、重要な後者2つを作っていない。
4. **Retrieval（取り出し）は「フィルタ」であるべき**: 関連しそうなものを全部入れるのではなく、「この事実が今の回答を変えるか？」で厳選する。書き込みは寛大に、読み込みは厳しく。
5. **モデルに「判断」、システムに「保存決定」を任せる**: モデルに「これ覚えとくべき？」と聞くのは危険。モデルは提案だけさせ、別のルール（プライバシー・重複チェック等）で本当に保存するか決める。
6. **削除が最も重要な操作**: 追加しかできないシステムは信用できない。ユーザーが「忘れて」と言ったら本当に消し、派生した情報も一緒に消す仕組みが必要。
7. **古くなる問題を無視しない**: 事実にはタイムスタンプを付け、定期的に「まだ正しいか」を確認する。古い情報を自動で優先順位下げたり期限切れにする仕組みが必要。

**いつ記憶システムが必要か**: 同じユーザーが戻ってくる場合／個人化の価値が高い場合／正しく忘れることが重要な場合。一回きりのタスクなら普通のコンテキストウィンドウで十分。

**結論**: Prompt engineering（メッセージを良くする）→ Context engineering（1回の呼び出しで何を見せるか制御）→ Memory engineering（呼び出しが終わった後も何を覚えているか制御）の3層が揃って初めて、エージェントは「毎回初対面」を卒業できる。

本VaultのプロジェクトルートにあるCLAUDE.md（プロジェクト永続コンテキスト）とAI駆動の`memory/`システムは、このSemantic memory（永続的な事実の記憶）に相当する実践例といえる。より広い業界動向（メモリの種類の分類・Mem0/OpenClaw等の実装・LLM-Wikiエコシステム）は別ソースの[[エージェントメモリ設計]]にまとめている。

## Claude Codeを他社APIで利用する（ゲートウェイ運用メモ）

Python製の自作ゲートウェイ（`ai-provider-gateway`）経由でGroq・OpenRouter等の無料/代替プロバイダーをClaude Code互換で使う運用と、Anthropic公式APIに直接接続する設定の切り替えメモ。

```powershell
cd C:\Users\marupon\PycharmProjects\ai-provider-gateway
git pull origin main
.\scripts\run-claude.ps1          # ゲートウェイ経由（Groq, OpenRouter等）
.\scripts\run-claude-direct.ps1   # Anthropic API に直接接続
```

ゲートウェイを経由せず直接Anthropic APIと通信する場合は、セッションから環境変数を削除する。

```powershell
Remove-Item Env:\ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
Remove-Item Env:\ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
```

## Claude Code + NotebookLM

Google NotebookLMにMCP経由で接続すると、Claude Codeはトークンを消費せずに完全なドキュメンテーションを読み込める。

## Claude Codeを無料/代替プロバイダーで動かすプロキシツール（free-claude-code）

`ai-provider-gateway`（自作ゲートウェイ、上記参照）とは別の、OSSのローカルプロキシツール。Claude Codeは通常どおりAnthropic形式のリクエストを送るだけで、`free-claude-code`がそれを任意のプロバイダーに転送する。

```
uv tool install git+https://github.com/Alishahryar1/free-claude-code
fcc-init  # 環境ファイルにAPIキーを入力
```

```
ANTHROPIC_BASE_URL = http://localhost:8082
ANTHROPIC_AUTH_TOKEN = freecc
```

CLI・VS Code拡張機能・JetBrainsいずれも設定変更不要。転送先の例: NVIDIA NIM（1分あたり40リクエスト無料）、OpenRouter、DeepSeek、Kimi、LM Studio/llama.cpp/Ollama（完全ローカル・オフライン）。Opus/Sonnet/Haikuをそれぞれ別のモデル・プロバイダーにマッピングできるため、高価なモデルの利用箇所を限定できる。

## Claude Code内からGrok 4.6を呼び出すプラグイン

Claude CodeやCodexのハーネスはそのまま使い、中の頭脳（モデル）だけをGrok 4.6に差し替えて動かす無料・オープンソースのプラグインが公開された。

- 必要条件はX PremiumまたはSuperGrokのアカウントのみ。OAuth連携だけで使える。
- 作者本人が24時間使い込み「速い・的確・無駄がない」と評価。
- 上記の`free-claude-code`（別プロバイダーへのプロキシ転送）とは異なり、ハーネス自体にモデル差し替えの仕組みを組み込むアプローチ。「単一モデル前提」のハーネス設計から一歩先に進んだ事例として言及されている。

## Claude + Obsidianで作る「自分で育つ第二の脳」

Claude CodeとObsidianを組み合わせた知識管理パターンについてのメモ集。**本Vault（second_brain）自体がこのパターンの実践例**にあたる。

- ソース（記事・PDF・メモ）を投げ込むだけでClaudeが内容を読み取り、人物・アイデアを抽出して相互リンク（wikilink）を張り、整理されたMarkdown Vaultに自動ファイルする、というコンセプト（Andrej Karpathyの「LLM Wiki」パターンがベース）。オープンソース・サブスクなし・データベースなし・ロックインなしで、プレーンなMarkdownとして所有できる。
- 日常的に使う主なコマンド（6種）: ①ソース1件投入→リンク付きページ自動生成、②複数ソース並列処理、③Vaultへの質問応答（引用付き）、④会話の永久ノート化、⑤自律的なWeb調査→ファイリング、⑥Vaultのクリーンアップ（孤立ページ・死リンク・矛盾検出）。本Vaultの`/ingest` `/query` `/lint`にそれぞれ対応する構成。
- 成長イメージ: 1日目は数ページの小さなグラフ、2週間後にリンクの網目ができ過去の知識を引用し始める、2ヶ月後にはGoogle検索の前に自分のVaultに聞くようになる。
- 便利なTips: PARA方式での分類、Web Clipperでの記事自動取り込み、週1回のリント、Obsidian Gitでの自動バックアップ。
- Obsidian創設者のkepano氏本人が公開しているSkillsも紹介されており、Markdown・Bases・JSON Canvas・バックリンク・プラグインなどObsidianの実際の慣習を尊重した実装として信頼度が高いとされる（`mattpocock/skills`のObsidian Vault Skillの派生版）。Claudeの`skills`フォルダに配置するだけで「このノートを要約して」等の指示から適切なスキルが自動起動する。
- 「保存（ライブラリ型）」と「コンパイル型」という2つの動作原理の違いとして同じパターンを捉え直した整理、具体的な運用プロンプト例、時間経過での効果（1ヶ月/3ヶ月/6ヶ月〜1年）、正直な限界は→[[セカンドブレインはストレージではなくコンパイラ]]を参照。

## エージェントをグラフとして設計する（Node/Edge思考）

直線的な「A→B→C→D」のプロンプトチェーンは退化したグラフに過ぎず、本当に強いエージェントシステムは**ノード（仕事の単位）**と**エッジ（データの依存関係、順番ではない）**で構成する、という設計論のメモ。

- 各ノードに入出力の形をスキーマで定義した「契約」を持たせ、構造化データとして返す
- `parallel()`で独立した仕事をファンアウトし、バリアで必要最小限だけファンイン
- 基本形は「ダイヤモンド構造」（split → work → merge）
- 条件分岐で実行時に動的ルーティング、エッジ上に検証ノード（敵対的検証・多視点検証）を置いて信頼性を上げる
- ノードを隔離し1つの失敗が全体を止めないようにする／収束条件つきのサイクルを許容する
- 簡単な仕事は安いモデル・判断が必要な部分は高性能モデルとノードごとにモデルを階層化し、トポロジーでコストと遅延を最適化する
- 最終形はClaude自身にオーケストレーショングラフを描かせる「自己ルーティング」

適用例として、セキュリティ監査・引用付き調査レポート・コード移植・差分の敵対的レビュー・定期的なエコシステム監視・未知のバグ探索が挙げられている。

具体的なノード構成例・トポロジーパターン・LangGraphでの実装コードは→[[グラフエンジニアリング]]を参照。

## 参考リンク

- Claude Code公式クイックスタート: <https://code.claude.com/docs/ja/quickstart>
- Claude Code逆引きリファレンス（非公式）: <https://claude-code-function.pages.dev/>

## 関連

- [[生成AIツール・リンク集]]
- [[クラウド・システムTips]]
- [[グラフエンジニアリング]] / [[ループエンジニアリング]]
- [[エージェントメモリ設計]]
- [[セカンドブレインはストレージではなくコンパイラ]]
- [[グラフエンジニアリング]]
