# -*- coding: utf-8 -*-
"""second_brain の /lint 用: リンク切れ・孤立ページの検出（検出のみ・修正しない）。

判定ロジック本体は find_wiki_issues.py（GrowLoop がテスト駆動で生成・検証した
純粋関数）にあり、このファイルは「どのファイルを読むか」「どのページを孤立判定
から除外するか」という second_brain 固有の運用ポリシーだけを担当する。

使い方（Vault のルートで実行）:

    python scripts/lint_links.py
    python scripts/lint_links.py C:\\path\\to\\vault   # ルートを明示する場合

出力は日本語のレポート。ファイルの書き換えは一切行わない
（`.claude/skills/lint/SKILL.md` の「検出・報告のみとし、自動修正は行わない」に従う）。
終了コードは、検出結果の有無に関わらず正常時 0。1 は実行エラー（Vault が無い等）。
"""

from __future__ import annotations

import sys
from pathlib import Path

from find_wiki_issues import find_wiki_issues

# リンクの収集対象（SKILL.md の Input と一致させる）。
# obsidian_vault/raw/ は人間のみが書く不変ソースのため対象外。
SCAN_DIRS = ("wiki", "obsidian_vault/daily", "weekly")

# 孤立ページとして報告する対象のディレクトリ。
# 日次ノート・週次レビューは他ページから参照されないのが通常のため除く。
ORPHAN_TARGET_DIR = "wiki"

# ハブ／ログとしての役割上、被リンクが無くても孤立とみなさないページ。
# 過去の /lint 実行（wiki/log.md の履歴）でも同じ扱いにしている。
HUB_PAGES = frozenset({"index", "log"})


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


def report(root: Path) -> int:
    pages, sources, collisions = collect_pages(root)
    if not pages:
        print(f"走査対象の Markdown が見つかりません（{root}）。")
        print(f"対象ディレクトリ: {', '.join(SCAN_DIRS)}")
        return 1

    result = find_wiki_issues(pages)

    # 孤立判定は wiki/ 配下のみを対象にし、ハブページは除く。
    orphan_dir = root / ORPHAN_TARGET_DIR
    orphans = [
        name
        for name in result["orphan_pages"]
        if name not in HUB_PAGES and orphan_dir in sources[name].parents
    ]
    broken = result["broken_links"]

    print(f"走査対象: {len(pages)} ファイル（{', '.join(SCAN_DIRS)}）")
    print()

    print(f"■ リンク切れ: {len(broken)} 件")
    if broken:
        for source_name, target in broken:
            origin = sources[source_name].relative_to(root)
            print(f"  - {origin} -> [[{target}]] （リンク先のページが存在しない）")
    else:
        print("  すべての wikilink が実在ページに解決しました。")
    print()

    print(f"■ 孤立ページ: {len(orphans)} 件")
    if orphans:
        for name in orphans:
            print(f"  - {sources[name].relative_to(root)} （どのページからもリンクされていない）")
    else:
        print(f"  {ORPHAN_TARGET_DIR}/ 配下に被リンクの無いページはありません。")
    print(f"  ※ ハブ／ログページ（{', '.join(sorted(HUB_PAGES))}）は対象外としています。")

    if collisions:
        print()
        print(f"■ 警告: ページ名の重複 {len(collisions)} 件")
        print("  同名ファイルがあるため、後から見つかった方を走査対象から除外しました。")
        for line in collisions:
            print(f"  - {line}")

    print()
    print("検出のみを行い、ファイルの修正は行っていません。")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        root = Path(argv[1]).expanduser().resolve()
    else:
        # scripts/ に置かれている前提で、リポジトリ（Vault）ルートを既定にする。
        root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"指定されたディレクトリが存在しません: {root}", file=sys.stderr)
        return 1
    return report(root)


if __name__ == "__main__":
    # Windows のコンソールは既定が cp932 のため、日本語出力で落ちないようにする。
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pragma: no cover - 環境依存
                pass
    raise SystemExit(main(sys.argv))
