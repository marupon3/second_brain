"""Hookのセルフテスト（ヘルスチェック）コマンド。

各Hookスクリプトへ「ブロックされるべき入力」「許可されるべき入力」を擬似的な
PreToolUse JSONとして標準入力から渡し、意図した通りに動作するかを確認する。

パターンマッチのロジックが正しいかではなく、実行環境でHookという仕組み
そのものが発火するかを検証する。2026-08-26に発覚した、python3コマンドが
存在しないWindows環境で全Hookが機構的に無効化されていた事故（全Hookが
python3をハードコードしており、フォールバックが無かった）の再発防止が
目的（docs/requirements.md 6節「Hookの動作確認」参照）。

終了コード:
    0 - すべてのHookが意図通り動作した
    1 - 少なくとも1つのHookが意図通り動作しなかった
    2 - 想定外のエラー
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from cli_common import configure_stdio_encoding, run_cli

HOOKS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "hooks"


@dataclass(frozen=True)
class HookCase:
    """1つのHookに対する「ブロックされるべき入力」と「許可されるべき入力」の組。"""

    script: str
    should_block: dict
    should_allow: dict


def build_cases() -> list[HookCase]:
    return [
        HookCase(
            script="block-raw-edit.sh",
            should_block={"tool_input": {"file_path": "obsidian_vault/raw/notes/test.md"}},
            should_allow={"tool_input": {"file_path": "wiki/test.md"}},
        ),
        HookCase(
            script="block-raw-bash.sh",
            should_block={"tool_input": {"command": "rm obsidian_vault/raw/notes/test.md"}},
            should_allow={"tool_input": {"command": "cat obsidian_vault/raw/notes/test.md"}},
        ),
        HookCase(
            script="block-secret-write.sh",
            # AIza + 35文字（block-secret-write.shのGoogle APIキー用パターンに一致させる）
            should_block={"tool_input": {"content": "key = AIza" + "a" * 35}},
            should_allow={"tool_input": {"content": "これは秘密情報を含まない通常のメモです。"}},
        ),
        HookCase(
            script="block-dangerous-git.sh",
            should_block={"tool_input": {"command": "git push --force origin main"}},
            should_allow={"tool_input": {"command": "git status"}},
        ),
    ]


def run_hook(script: str, payload: dict) -> tuple[int, str]:
    """Hookスクリプトへpayloadを標準入力として渡し、(終了コード, 標準出力)を返す。"""
    path = HOOKS_DIR / script
    result = subprocess.run(
        [str(path)],
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
    )
    return result.returncode, result.stdout.strip()


def is_denied(stdout: str) -> bool:
    """Hookの標準出力が「ブロック」を意味するJSONかどうかを判定する。"""
    if not stdout:
        return False
    try:
        data = json.loads(stdout)
    except ValueError:
        return False
    decision = (data.get("hookSpecificOutput") or {}).get("permissionDecision")
    return decision == "deny"


def check_case(case: HookCase) -> list[tuple[bool, str]]:
    results: list[tuple[bool, str]] = []

    code, stdout = run_hook(case.script, case.should_block)
    ok = code == 0 and is_denied(stdout)
    detail = (
        "ブロックを確認" if ok else f"ブロックされず（終了コード={code}, 出力={stdout or '(空)'}）"
    )
    results.append((ok, f"{case.script}: 危険な入力 → {detail}"))

    code, stdout = run_hook(case.script, case.should_allow)
    ok = code == 0 and not is_denied(stdout)
    if ok:
        detail = "許可を確認"
    else:
        detail = f"誤ってブロックされた（終了コード={code}, 出力={stdout or '(空)'}）"
    results.append((ok, f"{case.script}: 安全な入力 → {detail}"))

    return results


def run_checks() -> int:
    if not HOOKS_DIR.is_dir():
        print(f"Hookディレクトリが見つかりません: {HOOKS_DIR}", file=sys.stderr)
        return 2

    has_error = False
    for case in build_cases():
        for ok, message in check_case(case):
            print(f"[{'OK' if ok else 'NG'}] {message}")
            if not ok:
                has_error = True

    if has_error:
        print(
            "一部のHookが意図通り動作していません。"
            "python3またはpythonがPATHに存在するか確認してください"
            "（README.md「障害パターン別の初動」参照）。",
            file=sys.stderr,
        )
        return 1
    print("すべてのHookが意図通り動作していることを確認しました。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify_hooks.py",
        description="Hookが実行環境で意図通りにブロック/許可を行うかを確認する（パターンマッチの正しさではなく、機構が発火するかの確認）。",
    )
    parser.parse_args(argv)

    return run_cli(run_checks)


if __name__ == "__main__":
    configure_stdio_encoding()
    sys.exit(main())
