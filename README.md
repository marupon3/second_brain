# second-brain

Claude Code（Claude Codeエージェント）とObsidianを組み合わせた個人用の「第二の脳（Second Brain）」。
`obsidian_vault/raw/`に投入した生データから、AIが`wiki/`に構造化知識を継続的に生成・維持する、ローカル完結型の知識管理システム。
対象利用者は本Vaultを日常的に使う個人（単一ユーザー）。

## 前提環境

- OS: Windows 11（64bit）
- Python: 3.11.9（厳密固定。`pyproject.toml`の`requires-python`で指定）
- パッケージ管理: `uv`（主。仮想環境`venv`内にインストールする）、`pip`（フォールバック）
- Git
- Node.js（一部のClaude Code関連ツールで必要な場合のみ）
- Claude Code（Pro以上のプラン）
- Obsidian（最新安定版）

## セットアップ手順

1. 依存ツールの確認

   ```
   python scripts/check_env.py
   ```

   Python 3.11.9・Git・uv・pipが揃っているか確認する。不足があるとメッセージが表示され、終了コード1で終了する。

2. Vaultディレクトリ構造の生成

   ```
   python scripts/setup.py
   ```

   `obsidian_vault/raw/` `wiki/` `obsidian_vault/daily/` `weekly/` 等のディレクトリ構造を生成する（既存のファイル・ディレクトリは上書きしない）。カレントディレクトリ以外に生成したい場合は対象ディレクトリを引数で指定する。

   ```
   python scripts/setup.py C:\path\to\target
   ```

3. CLAUDE.mdを確認・カスタマイズする

   `CLAUDE.md`にAIの運用ルール（プロフィール・フォルダ構造・書き方ルール・禁止事項・優先Skills）が定義されている。必要に応じて内容を編集する。

4. Obsidianでこのフォルダを開く

   Obsidianの「フォルダを開く」からこのディレクトリを指定する。

5. Claude Codeをこのディレクトリで起動する

   ```
   cd second_brain
   claude
   ```

## 環境変数

現時点で必須の環境変数はない。将来的にMCPサーバー等が外部APIキーを必要とする場合は、`.env.example`をコピーして`.env`を作成し、値を設定すること（`.env`はコミットしない）。

```
copy .env.example .env
```

## 仮想環境（venv）とuvの運用ルール

本プロジェクトでは仮想環境フォルダ名を**`venv`（ドット無し）に固定**する。`.venv`は作成しない。

1. 仮想環境の作成とuvのインストール（uvはグローバルではなく`venv`内に入れる）

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   python -m pip install uv
   ```

2. `uv sync`等のuvプロジェクトコマンドは既定でプロジェクト直下の`.venv`を対象にし、有効化中の仮想環境を自動では見ない仕様のため、環境変数`UV_PROJECT_ENVIRONMENT`で`venv`を明示的に指定する（`.venv`が誤って新規作成されるのを防ぐ）。

   ```powershell
   setx UV_PROJECT_ENVIRONMENT "venv"
   ```

   `setx`はこれ以降に新しく開いたPowerShellから反映される。設定後はウィンドウを開き直し、`echo $env:UV_PROJECT_ENVIRONMENT`で`venv`と表示されることを確認する。

3. `venv`を作り直した場合は、手順1（uvの再インストール）を再度行う。

## 起動・利用コマンド

ビルドやテストの手順は無い（Markdownベースの知識ベースであり、ビルド成果物を持たない）。日常利用はClaude Code上でのSkills実行が中心となる。

- `/ingest` : `obsidian_vault/raw/`の新規ファイルを`wiki/`に構造化
- `/daily` : Daily Noteを生成・更新
- `/weekly` : Weekly Reviewを生成・更新
- `/lint` : リンク切れ・矛盾・孤立ページ・規約違反を検出（自動修正は行わない）
- `/query` : Vault全体を対象に質問応答
- `/dream` : `/lint`が記録した違反から、規約への昇格を提案する（適用には承認が必要）

## 学習ループ

`/lint`が検出した違反を`/dream`が規約へ昇格し、次回以降の`/ingest`がその規約を守った状態から
始まる、という1本のループを持つ。規約は`memory/conventions.md`に置かれ、生成系のSkillが
実行のたびに読む。

```
/ingest /daily /weekly  ->  /lint  ->  /dream  ->  人間が承認  ->  次回の生成が賢くなる
```

合否判定の経路にLLMを置かないため、違反の検出と再発回数の集計は決定的なスクリプトが担当する。

```
python scripts/lint_vault.py              # 規約違反を検出（検出のみ・修正しない）
python scripts/lint_vault.py --record     # 検出 + memory/violations.jsonl へ記録
python scripts/dream_memory.py            # 違反の再発回数を集計（読み取り専用）
python scripts/dream_memory.py --archive  # 規約へ昇格し終えた記録を退避する
```

これらの判定ロジック本体（`find_wiki_issues.py` `check_index_coverage.py`
`check_frontmatter.py` `check_skill_manifest.py` `summarize_violations.py`）は、
[GrowLoop](https://github.com/marupon3/GrowLoop)でテスト駆動生成・検証された純粋関数であり、
**手で編集しない**。仕様を変えたい場合はGrowLoop側のタスク定義を直して再生成する
（詳細はGrowLoopの`integrations/second_brain/README.md`）。

## ディレクトリ構成の要点

```
second_brain/
├── CLAUDE.md              # AI運用マニュアル
├── obsidian_vault/        # ユーザーが新たに情報を追加するフォルダ
│   ├── raw/                # 不変ソース（人間のみ編集）
│   ├── daily/               # 日次ノート
│   ├── projects/ areas/ resources/
├── wiki/                    # AI生成知識ベース
├── weekly/                  # 週次レビュー
├── templates/                # 固定テンプレート
├── .claude/skills/            # カスタムSkills定義
├── memory/                     # Skillsが実行のたびに読む規約と学習履歴
└── scripts/                    # 環境チェック・セットアップ・Vault検査用スクリプト
```

Obsidianはこの`second_brain/`フォルダ全体を1つのVaultとして開く。`obsidian_vault/`はその中で「人間が書き込む対象」を一段まとめたサブフォルダという位置づけ。

詳細なディレクトリ設計・Skills仕様は本Vaultの設計元となった基本設計書を参照（本リポジトリには同梱していない）。
