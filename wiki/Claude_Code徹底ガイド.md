---
title: Claude Code徹底ガイド
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2026-02-08 Claude.md
  - obsidian_vault/raw/notes/生成AI/2026-03-25 _Claude Code用Skills.md
  - obsidian_vault/raw/notes/生成AI/2026-03-25 _global Skills更新.md
  - obsidian_vault/raw/notes/生成AI/2026-07-29 _Claude Codeを他社APIで利用する.md
  - obsidian_vault/raw/notes/生成AI/無題.md
  - obsidian_vault/raw/notes/生成AI/2026-07-22 Clade Code + NotebookLM.md
  - obsidian_vault/raw/notes/生成AI/2026-02-19 _Claude Code公式.md
  - obsidian_vault/raw/notes/生成AI/2026-07-11 _Claude Code逆引き.md
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

## 参考リンク

- Claude Code公式クイックスタート: <https://code.claude.com/docs/ja/quickstart>
- Claude Code逆引きリファレンス（非公式）: <https://claude-code-function.pages.dev/>

## 関連

- [[生成AIツール・リンク集]]
- [[クラウド・システムTips]]
