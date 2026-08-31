# -*- coding: utf-8 -*-
"""GrowLoop の t09_find_wiki_issues と同じ契約を満たす判定ロジック。

このファイルは「GrowLoop が生成する成果物の置き場所」であり、手で編集しない。
現在の中身は GrowLoop の隠しテスト（別名記法・前後空白・重複リンク・自己リンクの
扱い、および docstring / None は ValueError / 引数を破壊しない、の 9 件）に
合格することを `growloop.verifier.verify()` で確認済みの実装。

仕様を変えたいときは GrowLoop 側の tasks/t09_find_wiki_issues.toml を直し、

    python -m growloop run --task t09_find_wiki_issues --provider ollama-cloud

で再生成した workspace/t09_find_wiki_issues/solution.py でこのファイルを丸ごと
置き換える（README の「ロジックを更新したいとき」を参照）。

ファイル入出力はしない（GrowLoop のサンドボックスが open/os を禁じており、
生成物は必ず純粋関数になるため）。実際のファイル読み込みは lint_links.py が行う。
"""

import re

_LINK_PATTERN = re.compile(r"\[\[\s*([^\]|]+?)\s*(?:\|[^\]]*)?\]\]")


def find_wiki_issues(pages: dict) -> dict:
    """Wikiページ間のリンク切れと孤立ページを検出した辞書を返す。

    pages は {ページ名: 本文テキスト} の dict。戻り値は
    {"broken_links": [(リンク元, リンク先), ...], "orphan_pages": [ページ名, ...]}
    で、いずれも昇順ソート済み。自分自身へのリンクは被参照とみなさない。
    """
    if pages is None:
        raise ValueError("pages に None は指定できません")

    incoming: set = set()
    broken: set = set()
    for name, content in pages.items():
        for target in _LINK_PATTERN.findall(content):
            if target == name:
                continue
            if target in pages:
                incoming.add(target)
            else:
                broken.add((name, target))
    orphan = sorted(name for name in pages if name not in incoming)
    return {"broken_links": sorted(broken), "orphan_pages": orphan}
