# -*- coding: utf-8 -*-
"""GrowLoop の t11_check_frontmatter と同じ契約を満たす判定ロジック。

このファイルは「GrowLoop が生成する成果物の置き場所」であり、手で編集しない。
現在の中身は GrowLoop の隠しテスト（必須キー欠落・frontmatter 無し・日付形式違反・
並び順・欠落と形式違反の二重計上をしないこと、および docstring / None は
ValueError、の 9 件）に合格することを `growloop.verifier.verify()` で確認済みの実装。

仕様を変えたいときは GrowLoop 側の tasks/t11_check_frontmatter.toml を直し、

    python -m growloop run --task t11_check_frontmatter --provider ollama-cloud

で再生成した workspace/t11_check_frontmatter/solution.py でこのファイルを丸ごと
置き換える（README の「ロジックを更新したいとき」を参照）。

ファイル入出力はしない（GrowLoop のサンドボックスが open/os を禁じており、
生成物は必ず純粋関数になるため）。実際のファイル読み込みは lint_vault.py が行う。
"""

import re


def check_frontmatter(pages: dict) -> dict:
    """各ページの frontmatter の必須キー欠落と日付形式違反を検出した辞書を返す。"""
    if pages is None:
        raise ValueError("pages に None は指定できません")
    required = ("title", "updated")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    missing = []
    invalid = []
    for name in sorted(pages):
        fields = {}
        lines = pages[name].splitlines()
        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if ":" in line:
                    key, value = line.split(":", 1)
                    fields[key.strip()] = value.strip()
        for key in required:
            if key not in fields:
                missing.append((name, key))
        updated = fields.get("updated")
        if updated is not None and not date_pattern.match(updated):
            invalid.append((name, updated))
    return {"missing_keys": missing, "invalid_dates": invalid}
