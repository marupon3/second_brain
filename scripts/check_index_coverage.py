# -*- coding: utf-8 -*-
"""GrowLoop の t10_check_index_coverage と同じ契約を満たす判定ロジック。

このファイルは「GrowLoop が生成する成果物の置き場所」であり、手で編集しない。
現在の中身は GrowLoop の隠しテスト（別名記法・前後空白・重複除去・両方向の
突き合わせ、および docstring / None は ValueError / 引数を破壊しない、の 9 件）に
合格することを `growloop.verifier.verify()` で確認済みの実装。

仕様を変えたいときは GrowLoop 側の tasks/t10_check_index_coverage.toml を直し、

    python -m growloop run --task t10_check_index_coverage --provider ollama-cloud

で再生成した workspace/t10_check_index_coverage/solution.py でこのファイルを丸ごと
置き換える（README の「ロジックを更新したいとき」を参照）。

ファイル入出力はしない（GrowLoop のサンドボックスが open/os を禁じており、
生成物は必ず純粋関数になるため）。実際のファイル読み込みは lint_vault.py が行う。
"""

import re


def check_index_coverage(page_names: list, index_body: str) -> dict:
    """index ページの掲載漏れと不存在リンクを検出した辞書を返す。"""
    if page_names is None:
        raise ValueError("page_names に None は指定できません")
    link_pattern = re.compile(r"\[\[\s*([^\]|]+?)\s*(?:\|[^\]]*)?\]\]")
    linked = set(link_pattern.findall(index_body))
    existing = set(page_names)
    missing = sorted(existing - linked)
    dangling = sorted(linked - existing)
    return {"missing_from_index": missing, "dangling_in_index": dangling}
