# -*- coding: utf-8 -*-
"""second_brain の /dream 用: 違反記録を集計し、規約へ昇格すべき再発パターンを示す。

役割分担（GrowLoop の Dreaming 設計をそのまま持ち込んでいる）:

    このスクリプト  何が何回の実行で再発したかを数える（決定的・読み取り専用）
    /dream (LLM)    その事実をもとに「規約としてどう書くか」の文言を起こす
    人間            提案に納得したときだけ memory/conventions.md への追記を許可する

数える処理を LLM にやらせないのは、GrowLoop が「合否判定の経路に LLM を登場させない」
という原則で設計されているのと同じ理由による。集計ロジック本体は GrowLoop が
テスト駆動で生成・検証した summarize_violations.py にあり、このファイルは
ファイル入出力と second_brain 固有の運用ポリシーだけを担当する。

使い方（Vault のルートで実行）:

    python scripts/dream_memory.py
    python scripts/dream_memory.py --threshold 2
    python scripts/dream_memory.py --archive

--archive は、規約への昇格を適用し終えた後にのみ実行する。現在の違反記録を
memory/violations-consumed.jsonl へ退避し、memory/violations.jsonl を空に戻す。
同じ学びが次回以降も繰り返し提案されるのを防ぐためのもので、GrowLoop の
「取り込んだセッションログを consumed に記録し、scratch.md を空に戻す」に相当する。

終了コードは、検出結果の有無に関わらず正常時 0。1 は実行エラー。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from summarize_violations import summarize_violations

# 違反記録の読み取り元と、消化済み記録の退避先。
VIOLATIONS_LOG = "memory/violations.jsonl"
CONSUMED_LOG = "memory/violations-consumed.jsonl"

# 何回の実行で再発したら規約への昇格を検討するか。
# GrowLoop が「同一の失敗署名が 3 回連続」で進捗なしと判断するのに合わせている。
DEFAULT_THRESHOLD = 3

# 違反コードから、どういう性質の問題かを人間向けに補足する。
# 規約の文言そのものは /dream（LLM）が起こすため、ここには書かない。
CODE_HINTS = {
    "BROKEN_LINK": "リンク先の存在しない wikilink が書かれている",
    "ORPHAN_PAGE": "どのページからも参照されないページが生成されている",
    "INDEX_MISSING": "ページを作ったが wiki/index.md への追記が漏れている",
    "INDEX_DANGLING": "index が実在しないページを参照している",
    "FRONTMATTER_MISSING_KEY": "frontmatter の必須キーが欠けたページが生成されている",
    "FRONTMATTER_BAD_DATE": "日付の書式が YYYY-MM-DD に揃っていない",
    "SKILL_NAME_MISMATCH": "Skill の宣言名とディレクトリ名がずれている",
}


def load_records(path: Path) -> tuple[list[dict], list[int]]:
    """violations.jsonl を読み、レコードのリストと壊れた行の行番号を返す。"""
    records: list[dict] = []
    broken: list[int] = []
    if not path.is_file():
        return records, broken
    text = path.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            broken.append(number)
            continue
        if isinstance(row, dict):
            records.append(row)
        else:
            broken.append(number)
    return records, broken


def render(records: list[dict], broken: list[int], threshold: int) -> None:
    """集計結果を日本語で標準出力へ書き出す。"""
    runs = {row.get("detected_at") for row in records if row.get("detected_at")}
    print(f"違反記録: {len(records)} 件 / 検査の実行回数: {len(runs)} 回")
    if broken:
        print(f"※ 解釈できない行が {len(broken)} 行ありました（行番号: {broken}）。")
        print("  これらは無視して集計しています。")
    print(f"再発とみなすしきい値: {threshold} 回以上の実行で出現")
    print()

    if not records:
        print("違反記録がありません。まず /lint を実行して記録を貯めてください。")
        print("  python scripts/lint_vault.py --record")
        return

    result = summarize_violations(records, threshold)

    print(f"■ 規約への昇格候補（再発）: {len(result['recurring'])} 件")
    if result["recurring"]:
        for code, count in result["recurring"]:
            hint = CODE_HINTS.get(code, "")
            print(f"  - {code}: {count} 回の実行で出現" + (f" / {hint}" if hint else ""))
    else:
        print("  しきい値に達した違反はありません。")
    print()

    print(f"■ 単発（様子見）: {len(result['occasional'])} 件")
    if result["occasional"]:
        for code, count in result["occasional"]:
            hint = CODE_HINTS.get(code, "")
            print(f"  - {code}: {count} 回の実行で出現" + (f" / {hint}" if hint else ""))
    else:
        print("  該当なし。")
    print()

    print("このスクリプトは数えるだけで、memory/ への書き込みは行っていません。")
    print("規約の文言起こしと提案は /dream が、適用の可否は人間が判断します。")


def archive(root: Path) -> int:
    """消化済みの違反記録を退避し、violations.jsonl を空に戻す。"""
    source = root / VIOLATIONS_LOG
    if not source.is_file():
        print(f"{VIOLATIONS_LOG} がありません。退避するものはありません。")
        return 0
    text = source.read_text(encoding="utf-8")
    if not text.strip():
        print(f"{VIOLATIONS_LOG} は既に空です。")
        return 0

    target = root / CONSUMED_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(text if text.endswith("\n") else text + "\n")
    source.write_text("", encoding="utf-8", newline="\n")

    moved = len([line for line in text.splitlines() if line.strip()])
    print(f"違反記録 {moved} 件を {CONSUMED_LOG} へ退避し、{VIOLATIONS_LOG} を空にしました。")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="dream_memory.py",
        description="違反記録を集計し、規約へ昇格すべき再発パターンを示す（読み取り専用）。",
        # 省略形の誤解釈で意図しないオプションが黙って通るのを防ぐ。
        allow_abbrev=False,
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Vault のルート。省略時は scripts/ の親ディレクトリ。",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"再発とみなす実行回数のしきい値（既定 {DEFAULT_THRESHOLD}）。",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="規約へ昇格し終えた後に、違反記録を消化済みへ退避して空に戻す。",
    )
    args = parser.parse_args(argv[1:])

    if args.root is not None:
        root = Path(args.root).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"指定されたディレクトリが存在しません: {root}", file=sys.stderr)
        return 1
    if args.threshold < 1:
        print("--threshold は 1 以上を指定してください。", file=sys.stderr)
        return 1

    if args.archive:
        return archive(root)

    records, broken = load_records(root / VIOLATIONS_LOG)
    render(records, broken, args.threshold)
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
