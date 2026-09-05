# -*- coding: utf-8 -*-
"""GrowLoop の t12_check_skill_manifest と同じ契約を満たす判定ロジック。

このファイルは「GrowLoop が生成する成果物の置き場所」であり、手で編集しない。
現在の中身は GrowLoop の隠しテスト（宣言名の不一致・一致時は無報告・name 行が
無い場合・frontmatter が無い場合・並び順、および docstring / None は ValueError、
の 9 件）に合格することを `growloop.verifier.verify()` で確認済みの実装。

仕様を変えたいときは GrowLoop 側の tasks/t12_check_skill_manifest.toml を直し、

    python -m growloop run --task t12_check_skill_manifest --provider ollama-cloud

で再生成した workspace/t12_check_skill_manifest/solution.py でこのファイルを丸ごと
置き換える（README の「ロジックを更新したいとき」を参照）。

ファイル入出力はしない（GrowLoop のサンドボックスが open/os を禁じており、
生成物は必ず純粋関数になるため）。実際のファイル読み込みは lint_vault.py が行う。
"""


def check_skill_manifest(skills: dict) -> list:
    """Skill 定義の宣言名とディレクトリ名の不一致を列挙したリストを返す。"""
    if skills is None:
        raise ValueError("skills に None は指定できません")
    mismatches = []
    for directory in sorted(skills):
        lines = skills[directory].splitlines()
        declared = ""
        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("name:"):
                    declared = line.split(":", 1)[1].strip()
                    break
        if declared != directory:
            mismatches.append((directory, declared))
    return mismatches
