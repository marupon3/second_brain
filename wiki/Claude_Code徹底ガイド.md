---
title: Claude Code徹底ガイド
updated: 2026-08-18
source:
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
  - obsidian_vault/raw/notes/Claude Skills 72選.md
  - obsidian_vault/raw/notes/Graph enginering.md
  - "obsidian_vault/raw/notes/claude Code/2026-08-18 Grok 4.6をそのまま呼び出せるプラグイン.md"
---

# Claude Code徹底ガイド

「Master Claude Code」（Aakash Gupta, v1.0 2026年1月）等のガイド記事・実体験メモをまとめたもの。

## Claude Codeの位置づけ

チャットツールではなく、ワークフロー全体で動く「OS層」に近い。フルなファイルシステムアクセス、アップロード上限なし、数時間単位のタスク実行、MCP経由で外部ツールと連携できる点が従来のチャットAIとの違い。

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
- [[グラフエンジニアリング]]
