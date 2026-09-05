# -*- coding: utf-8 -*-
"""GrowLoop の t13_summarize_violations と同じ契約を満たす集計ロジック。

このファイルは「GrowLoop が生成する成果物の置き場所」であり、手で編集しない。
現在の中身は GrowLoop の隠しテスト（実行回数で数えること・しきい値での切り分け・
並び順・壊れた記録の無視・しきい値の検証、および docstring / None は ValueError /
引数を破壊しない、の 9 件）に合格することを `growloop.verifier.verify()` で確認済み。

仕様を変えたいときは GrowLoop 側の tasks/t13_summarize_violations.toml を直し、

    python -m growloop run --task t13_summarize_violations --provider ollama-cloud

で再生成した workspace/t13_summarize_violations/solution.py でこのファイルを丸ごと
置き換える（README の「ロジックを更新したいとき」を参照）。

ファイル入出力はしない（GrowLoop のサンドボックスが open/os を禁じており、
生成物は必ず純粋関数になるため）。実際のファイル読み込みは dream_memory.py が行う。
"""


def summarize_violations(records: list, threshold: int) -> dict:
    """違反記録を種類ごとに集計し、再発しているものと単発のものに分けて返す。"""
    if records is None:
        raise ValueError("records に None は指定できません")
    if threshold < 1:
        raise ValueError("threshold は 1 以上を指定してください")
    runs = {}
    for item in records:
        code = item.get("code")
        detected_at = item.get("detected_at")
        if code is None or detected_at is None:
            continue
        runs.setdefault(code, set()).add(detected_at)
    counted = [(code, len(stamps)) for code, stamps in runs.items()]
    counted.sort(key=lambda pair: (-pair[1], pair[0]))
    recurring = [pair for pair in counted if pair[1] >= threshold]
    occasional = [pair for pair in counted if pair[1] < threshold]
    return {"recurring": recurring, "occasional": occasional}
