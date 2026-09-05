---
name: lint
description: wiki/等のリンク切れ・矛盾・孤立ページ・規約違反を検出し報告する。自動修正は行わない。ユーザーが/lintを実行したときに使用する。
---

# lint

## When to use

- ユーザーが `/lint` を実行したとき
- Vaultの整合性を定期的に確認したいとき
- `/ingest` `/daily` `/weekly` でページを生成・更新した直後（生成物が規約を守れているかの確認）

## When not to use

- `wiki/`にページが1件も無いとき

## Input

- `wiki/` `obsidian_vault/daily/` `weekly/` 配下の全Markdownファイル
- `.claude/skills/*/SKILL.md`
- `memory/conventions.md`（何が違反かの定義。各項目の`[CODE]`が検出結果と対応する）

## Output

- 検出結果のレポート（`wiki/log.md`への追記、および必要に応じて`wiki/lint-report.md`）
- `memory/violations.jsonl`への違反記録の追記（`--record`による。`/dream`の入力になる）

## 手順

1. `python scripts/lint_vault.py --record` を実行し、規約違反の検出結果を得る。

   このスクリプトは決定的に動作する（GrowLoopでテスト駆動生成・検証済みの純粋関数
   `find_wiki_issues` / `check_index_coverage` / `check_frontmatter` /
   `check_skill_manifest` を使う）ため、**結果をそのまま採用してよい**。
   wikilinkの再パースやfrontmatterの解釈を自前でやり直さない。

   検出される違反は次の7種類。いずれも`memory/conventions.md`の項目と1対1で対応する。

   | コード | 意味 |
   |---|---|
   | `BROKEN_LINK` | リンク先が存在しないwikilink |
   | `ORPHAN_PAGE` | どのページからも参照されていない`wiki/`ページ |
   | `INDEX_MISSING` | `wiki/index.md`のトピック一覧への掲載漏れ |
   | `INDEX_DANGLING` | `wiki/index.md`が実在しないページを参照 |
   | `FRONTMATTER_MISSING_KEY` | frontmatterに`title`または`updated`が無い |
   | `FRONTMATTER_BAD_DATE` | `updated`が`YYYY-MM-DD`形式でない |
   | `SKILL_NAME_MISMATCH` | SKILL.mdの`name`とディレクトリ名の不一致 |

   `--record`は検出結果を`memory/violations.jsonl`へ追記する。これは`/dream`が
   「同じ違反が何回の実行で再発したか」を数えるための入力であり、Vaultの内容
   （`wiki/`等）には一切書き込まない。

2. 同一トピックについて内容が相反する可能性のある記述を検出する。これは解釈を要する
   ため、スクリプトではなくこのSkill（LLM）が担当する。判断が難しい場合は断定せず、
   AIの所見として記録するに留める。

3. 1のスクリプト出力と2の所見を一覧化し、`wiki/log.md`に追記する。件数が多い場合は
   `wiki/lint-report.md`に詳細を出力する。違反コードは省略せず記載する（後から
   `/dream`の集計結果と突き合わせられるようにするため）。

4. 検出件数が0でない場合、`/dream`で規約への昇格を検討できる旨をユーザーに伝える。
   ただし`/dream`をこのSkillから自動実行はしない。

## 制約

- **検出・報告のみとし、自動修正は行わない**（`docs/requirements.md` 6節Q3。誤修正リスクを避けるため）。
- 修正はユーザー自身の判断に委ねる（手動修正、またはユーザーがClaudeへ個別に修正を指示する）。
- `obsidian_vault/raw/`配下のファイルを編集しない。
- `memory/conventions.md` `memory/lessons.md` をこのSkillから書き換えない（`/dream`と人間の承認を経る）。
- 書き込んでよいのは`wiki/log.md`（および`wiki/lint-report.md`）と、`--record`による
  `memory/violations.jsonl`だけ。
- スクリプトが検出した違反を「誤検知」として黙って握りつぶさない。仕様が誤っていると
  判断した場合は、`memory/conventions.md`と対応するGrowLoop側のタスク定義を直す。
- 出力は日本語で書く。
- ファイル入出力時はエンコーディングを UTF-8 で明示する。
- コンソール出力以外で絵文字を使わない。
