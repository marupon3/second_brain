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
- `/lint` : リンク切れ・矛盾・孤立ページを検出（自動修正は行わない）
- `/query` : Vault全体を対象に質問応答

## 運用・トラブル対応

サーバーを持たないローカル完結型のため、デプロイ・監視基盤・アラート通知といった運用は存在しない。日常運用で必要になるのは以下のみ。

### 変更の切り戻し

`git reset --hard`のような破壊的コマンドは使わず、履歴を壊さない手順で戻す（`git push --force`・`git reset --hard`・`git clean -f`系・`git checkout/restore .`・`git branch -D`はClaude Code側からは`.claude/hooks/block-dangerous-git.sh`でブロックされる。詳細は「Hookによる保護」参照）。

1. `git log`で問題発生前のコミットを特定する
2. `git revert <コミットID>`で当該変更を打ち消す新しいコミットを作成する
3. Obsidian側で開いているファイルがあれば再読み込みする

### Hookによる保護

`.claude/hooks/`にPreToolUse Hookを配置し、`.claude/settings.json`から登録している。ガイダンス（`CLAUDE.md`の記述）だけでは100%守られる保証がないため、取り返しのつかない操作は機構的にブロックする。

| Hook | ブロックする内容 |
|---|---|
| `block-raw-edit.sh` | `obsidian_vault/raw/`配下へのEdit/Write/NotebookEdit |
| `block-raw-bash.sh` | `obsidian_vault/raw/`配下を対象にした`rm`/`mv`/`sed -i`等 |
| `block-secret-write.sh` | APIキーらしき文字列（Google/Anthropic/GitHub/AWS/OpenAI形式）の書き込み |
| `block-dangerous-git.sh` | `git push --force`・`git reset --hard`・`git clean -f`系・`git checkout/restore .`・`git branch -D` |

いずれもWindows環境に`jq`が無いことを前提に、Python 3（前提環境参照）でJSON入出力を行う実装になっている。`obsidian_vault/private/**`の読み取り拒否は`.claude/settings.json`の`permissions.deny`で別途設定している。

### バックアップとリストア

- 取得方法: Gitコミット、またはVaultフォルダ全体のコピー
- 保存先: ローカルのGitリポジトリ、または任意の外部ストレージ
- リストア: Gitなら`git clone`するか対象コミットへ`git checkout <コミットID>`する。フォルダコピーならバックアップしたフォルダ全体を復元先にコピーする

`obsidian_vault/private/`は`.gitignore`で除外されGitに含まれないため、フォルダコピーで別途退避する。

### 障害パターン別の初動

| 事象 | 初動 |
|---|---|
| `check_env.py`が終了コード1で終了する | 出力の`[NG]`行から不足しているツール（Python 3.11.9 / Git / uv / pip）を特定し、導入またはバージョンを合わせて再実行する |
| `setup.py`が「対象パスがディレクトリではありません」で終了する | 指定した対象パスが既存ファイルと衝突していないか確認し、正しいディレクトリパスを指定し直す |
| `obsidian_vault/raw/`がAIに編集された疑いがある | `git diff -- obsidian_vault/raw/`で内容を確認し、意図しない変更なら`git checkout -- <該当ファイル>`（コミット前）または`git revert`（コミット後）で復元する |
| `/lint`がリンク切れ・矛盾を検出した | 自動修正は行わない設計のため、手動で修正するか、Claude Codeに個別に修正を指示する |
| Skillsの応答が目安より大幅に遅い | `wiki/`のページ数を確認する。インデックスを持たずファイルシステムを直接走査する設計のため、ページ数の増加がそのまま処理時間に効く |
| Claude Codeが実行したコマンドで`python3: command not found`（終了コード127） | このWindows環境のgit-bashには`python3`という名前のコマンドが無い。`python`または仮想環境の`venv\Scripts\python`を使う |

処理時間の目安は、`/ingest`が1件あたり30〜90秒、`/query`が10〜30秒、`/lint`が数百ページ規模で1〜3分、`/daily`が10秒以内。

### 実行履歴

Skillsの実行履歴は`wiki/log.md`に追記される。スクリプトは標準出力・標準エラーにのみ出力し、永続的なログファイルは生成しない。

## ディレクトリ構成の要点

```
second_brain/
├── CLAUDE.md              # AI運用マニュアル
├── obsidian_vault/        # ユーザーが新たに情報を追加するフォルダ
│   ├── raw/                # 不変ソース（人間のみ編集）
│   ├── daily/               # 日次ノート
│   ├── private/             # ローカル専用（.gitignoreで除外、リモート非同期）
│   └── templates/          # 固定テンプレート
├── wiki/                    # AI生成知識ベース
├── weekly/                  # 週次レビュー
├── .claude/skills/            # カスタムSkills定義
├── .claude/hooks/              # 破壊的操作・秘密情報書き込みを機構的にブロックするHook
└── scripts/                    # 環境チェック・セットアップ用スクリプト
```

Obsidianアプリで開くVaultルートは`second_brain/`全体ではなく**`obsidian_vault/`**（`.obsidian/`設定フォルダは`obsidian_vault/.obsidian/`にのみ存在）。`wiki/`・`weekly/`はリポジトリ直下にあり`obsidian_vault/`の外＝Vault外のため、Obsidianアプリからは見えずwikilinkも解決されない。両フォルダはClaude Code CLI（Skills）が直接読み書きするAI運用専用ディレクトリであり、Obsidianアプリでの閲覧は想定しない。

詳細なディレクトリ設計・Skills仕様は本Vaultの設計元となった基本設計書を参照（本リポジトリには同梱していない）。
