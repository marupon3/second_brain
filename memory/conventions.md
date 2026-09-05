# 規約（検証済み）

このファイルは Skills が**実行のたびに読む恒久ルール**である。`CLAUDE.md` が
「このリポジトリ全体の運用方針」を定めるのに対し、こちらは「生成物が満たすべき、
機械的に検証できる条件」だけを書く。

各項目の末尾の `[CODE]` は、`scripts/lint_vault.py` が違反を検出したときに出す
違反コードを指す。**コードの無い規約はここに書かない。** 検証手段の無いルールを
足すと、守られているかどうかを誰も確認できないまま増え続けるためである
（GrowLoop の設計原則: 合否は LLM の自己申告ではなく実際の検査で決める）。

書き換えの経路は 2 つだけ:

- `/dream` の提案を人間が承認したとき（`memory/proposals/` 参照）
- 人間が直接編集したとき

## 一覧

- `wiki/` にページを新規作成したら、必ず `wiki/index.md` のトピック一覧へ
  wikilink を追記する。追記を忘れたページは目次から辿れなくなる。 [INDEX_MISSING]
- `wiki/index.md` から参照するページは実在するものに限る。ページを削除・改名
  したら index 側の記述も同時に直す。 [INDEX_DANGLING]
- `wiki/` の全ページは、他のいずれかのページから wikilink で参照される状態にする。
  どこからも参照されないページを作らない（`index` と `log` はハブのため対象外）。 [ORPHAN_PAGE]
- wikilink `[[ページ名]]` のリンク先は、実在するページ名と正確に一致させる。
  存在しないページ名を先に書かない。 [BROKEN_LINK]
- `wiki/` `obsidian_vault/daily/` `weekly/` の全 Markdown は、先頭に
  `title` と `updated` を持つ frontmatter を置く。 [FRONTMATTER_MISSING_KEY]
- frontmatter の `updated` は `YYYY-MM-DD` 形式で書く（`2026/08/06` や
  `2026-8-6` は不可）。 [FRONTMATTER_BAD_DATE]
- `.claude/skills/<名前>/SKILL.md` の frontmatter の `name` は、その
  ディレクトリ名と完全に一致させる。 [SKILL_NAME_MISMATCH]
