# -*- coding: utf-8 -*-
"""second_brain の /lint 用: Vault の規約違反を決定的に検出する（検出のみ・修正しない）。

判定ロジック本体は GrowLoop がテスト駆動で生成・検証した 4 つの純粋関数にある。

    find_wiki_issues      リンク切れ・孤立ページ            (t09)
    check_index_coverage  index の掲載漏れ・不存在リンク    (t10)
    check_frontmatter     frontmatter の欠落・日付形式違反  (t11)
    check_skill_manifest  Skill 宣言名とディレクトリ名の齟齬 (t12)

このファイルが担当するのは「どのファイルを読むか」「どれを除外するか」という
second_brain 固有の運用ポリシーだけであり、判定そのものは行わない。

使い方（Vault のルートで実行）:

    python scripts/lint_vault.py
    python scripts/lint_vault.py --root C:\\path\\to\\vault
    python scripts/lint_vault.py --record

--record は検出結果を機械可読な違反記録として memory/violations.jsonl へ追記する。
これは /dream が「同じ違反が何回繰り返されたか」を数えるための入力であり、
Vault の内容（wiki/ 等）には一切書き込まない。

終了コードは、検出結果の有無に関わらず正常時 0。1 は実行エラー（Vault が無い等）。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from check_frontmatter import check_frontmatter
from check_index_coverage import check_index_coverage
from check_skill_manifest import check_skill_manifest
from find_wiki_issues import find_wiki_issues

# --------------------------------------------------------------- 運用ポリシー

# wikilink の収集対象（lint/SKILL.md の Input と一致させる）。
# obsidian_vault/raw/ は人間のみが書く不変ソースのため対象外。
SCAN_DIRS = ("wiki", "obsidian_vault/daily", "weekly")

# 孤立ページ・index 掲載漏れとして報告する対象のディレクトリ。
# 日次ノート・週次レビューは他ページから参照されないのが通常のため除く。
WIKI_DIR = "wiki"

# ハブ／ログとしての役割上、被リンクが無くても孤立とみなさないページ。
# index 自身の掲載対象からも外す。
HUB_PAGES = frozenset({"index", "log"})

# index（カタログ）ページ。掲載漏れの突き合わせ元。
INDEX_PAGE = "wiki/index.md"

# Skill 定義の置き場所。
SKILLS_DIR = ".claude/skills"

# 違反記録の追記先。Vault の内容ではなくメモリ側に置く。
VIOLATIONS_LOG = "memory/violations.jsonl"

# 違反コード。/dream はこの文字列で違反を数えるため、一度決めたら変えない。
CODE_BROKEN_LINK = "BROKEN_LINK"
CODE_ORPHAN_PAGE = "ORPHAN_PAGE"
CODE_INDEX_MISSING = "INDEX_MISSING"
CODE_INDEX_DANGLING = "INDEX_DANGLING"
CODE_FRONTMATTER_MISSING_KEY = "FRONTMATTER_MISSING_KEY"
CODE_FRONTMATTER_BAD_DATE = "FRONTMATTER_BAD_DATE"
CODE_SKILL_NAME_MISMATCH = "SKILL_NAME_MISMATCH"

# 表示用の見出し。宣言順がそのままレポートの節の順になる。
SECTIONS = (
    (CODE_BROKEN_LINK, "リンク切れ"),
    (CODE_ORPHAN_PAGE, "孤立ページ"),
    (CODE_INDEX_MISSING, "index への掲載漏れ"),
    (CODE_INDEX_DANGLING, "index からの不存在リンク"),
    (CODE_FRONTMATTER_MISSING_KEY, "frontmatter の必須キー欠落"),
    (CODE_FRONTMATTER_BAD_DATE, "frontmatter の日付形式違反"),
    (CODE_SKILL_NAME_MISMATCH, "Skill 宣言名とディレクトリ名の不一致"),
)


def collect_pages(root: Path) -> tuple[dict[str, str], dict[str, Path], list[str]]:
    """走査対象の Markdown を読み、{ページ名: 本文} と {ページ名: パス} を返す。

    ページ名は wikilink の書き方に合わせて拡張子を除いたファイル名とする
    （wiki/obsidian.md なら "obsidian"）。ディレクトリ違いで同名のファイルが
    あると片方が隠れてしまうため、衝突は警告として返す。
    """
    pages: dict[str, str] = {}
    sources: dict[str, Path] = {}
    collisions: list[str] = []

    for rel_dir in SCAN_DIRS:
        directory = root / rel_dir
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            name = path.stem
            if name in pages:
                collisions.append(
                    f"{name}: {sources[name].relative_to(root)} と {path.relative_to(root)}"
                )
                continue
            pages[name] = path.read_text(encoding="utf-8")
            sources[name] = path

    return pages, sources, collisions


def collect_skills(root: Path) -> dict[str, str]:
    """{Skill ディレクトリ名: SKILL.md の本文} を返す。SKILL.md が無いものは除く。"""
    skills: dict[str, str] = {}
    skills_root = root / SKILLS_DIR
    if not skills_root.is_dir():
        return skills
    for directory in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        manifest = directory / "SKILL.md"
        if manifest.is_file():
            skills[directory.name] = manifest.read_text(encoding="utf-8")
    return skills


def _violation(code: str, location: str, detail: str) -> dict[str, str]:
    return {"code": code, "location": location, "detail": detail}


def find_violations(root: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Vault を走査し、検出した違反のリストと表示用の付帯情報を返す。"""
    pages, sources, collisions = collect_pages(root)
    violations: list[dict[str, str]] = []

    wiki_dir = root / WIKI_DIR

    def in_wiki(name: str) -> bool:
        return name in sources and wiki_dir in sources[name].parents

    def where(name: str) -> str:
        return str(sources[name].relative_to(root)) if name in sources else name

    # --- t09: リンク切れ・孤立ページ -------------------------------------
    link_result = find_wiki_issues(pages)
    for origin, target in link_result["broken_links"]:
        violations.append(
            _violation(
                CODE_BROKEN_LINK,
                where(origin),
                f"[[{target}]] のリンク先ページが存在しない",
            )
        )
    for name in link_result["orphan_pages"]:
        # 孤立判定は wiki/ 配下のみを対象にし、ハブページは除く。
        if name in HUB_PAGES or not in_wiki(name):
            continue
        violations.append(
            _violation(CODE_ORPHAN_PAGE, where(name), "どのページからもリンクされていない")
        )

    # --- t10: index の掲載漏れ・不存在リンク ------------------------------
    index_path = root / INDEX_PAGE
    if index_path.is_file():
        index_body = index_path.read_text(encoding="utf-8")
        wiki_pages = [n for n in pages if in_wiki(n) and n not in HUB_PAGES]
        index_result = check_index_coverage(wiki_pages, index_body)
        for name in index_result["missing_from_index"]:
            violations.append(
                _violation(
                    CODE_INDEX_MISSING,
                    where(name),
                    f"{INDEX_PAGE} のトピック一覧に掲載されていない",
                )
            )
        for name in index_result["dangling_in_index"]:
            violations.append(
                _violation(
                    CODE_INDEX_DANGLING,
                    INDEX_PAGE,
                    f"[[{name}]] を参照しているが wiki/ に該当ページが無い",
                )
            )

    # --- t11: frontmatter -------------------------------------------------
    front_result = check_frontmatter(pages)
    for name, key in front_result["missing_keys"]:
        violations.append(
            _violation(CODE_FRONTMATTER_MISSING_KEY, where(name), f"必須キー {key} が無い")
        )
    for name, value in front_result["invalid_dates"]:
        violations.append(
            _violation(
                CODE_FRONTMATTER_BAD_DATE,
                where(name),
                f"updated: {value} が YYYY-MM-DD 形式でない",
            )
        )

    # --- t12: Skill 定義 --------------------------------------------------
    skills = collect_skills(root)
    for directory, declared in check_skill_manifest(skills):
        shown = declared if declared else "(name の宣言が無い)"
        violations.append(
            _violation(
                CODE_SKILL_NAME_MISMATCH,
                f"{SKILLS_DIR}/{directory}/SKILL.md",
                f"ディレクトリ名は {directory} だが name は {shown}",
            )
        )

    context: dict[str, object] = {
        "scanned": len(pages),
        "collisions": collisions,
        "skills": len(skills),
        "has_index": index_path.is_file(),
    }
    return violations, context


def render(violations: list[dict[str, str]], context: dict[str, object]) -> None:
    """検出結果を日本語のレポートとして標準出力へ書き出す。"""
    print(f"走査対象: {context['scanned']} ファイル（{', '.join(SCAN_DIRS)}）")
    print(f"Skill 定義: {context['skills']} 件（{SKILLS_DIR}）")
    if not context["has_index"]:
        print(f"※ {INDEX_PAGE} が見つからないため、掲載漏れの検査は行っていません。")
    print()

    by_code: dict[str, list[dict[str, str]]] = {}
    for item in violations:
        by_code.setdefault(item["code"], []).append(item)

    for code, label in SECTIONS:
        found = by_code.get(code, [])
        print(f"■ {label}[{code}]: {len(found)} 件")
        for item in found:
            print(f"  - {item['location']} : {item['detail']}")
    print()

    collisions = context["collisions"]
    if collisions:
        print(f"■ 警告: ページ名の重複 {len(collisions)} 件")
        print("  同名ファイルがあるため、後から見つかった方を走査対象から除外しました。")
        for line in collisions:  # type: ignore[union-attr]
            print(f"  - {line}")
        print()

    print(f"合計 {len(violations)} 件の違反を検出しました。")
    print("検出のみを行い、ファイルの修正は行っていません。")


def record(root: Path, violations: list[dict[str, str]]) -> Path:
    """違反を memory/violations.jsonl へ 1 件 1 行の JSON として追記する。

    /dream が違反コードごとの再発回数を数えるための入力。Vault の内容は変更しない。
    """
    path = root / VIOLATIONS_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    detected_at = datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for item in violations:
            row = {"detected_at": detected_at, **item}
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="lint_vault.py",
        description="Vault の規約違反を決定的に検出する（検出のみ・修正しない）。",
        # 省略形の誤解釈で意図しないオプションが黙って通るのを防ぐ。
        allow_abbrev=False,
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Vault のルート。省略時は scripts/ の親ディレクトリ。",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help=f"検出結果を {VIOLATIONS_LOG} へ追記する（/dream の入力になる）。",
    )
    args = parser.parse_args(argv[1:])

    if args.root is not None:
        root = Path(args.root).expanduser().resolve()
    else:
        # scripts/ に置かれている前提で、リポジトリ（Vault）ルートを既定にする。
        root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"指定されたディレクトリが存在しません: {root}", file=sys.stderr)
        return 1

    violations, context = find_violations(root)
    if not context["scanned"]:
        print(f"走査対象の Markdown が見つかりません（{root}）。", file=sys.stderr)
        print(f"対象ディレクトリ: {', '.join(SCAN_DIRS)}", file=sys.stderr)
        return 1

    render(violations, context)
    if args.record:
        path = record(root, violations)
        print()
        print(f"違反 {len(violations)} 件を {path.relative_to(root)} へ記録しました。")
    return 0


if __name__ == "__main__":
    # Windows のコンソールは既定が cp932 のため、日本語出力で落ちないようにする。
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pragma: no cover - 環境依存
                pass
    raise SystemExit(main(sys.argv))
