"""環境チェックコマンド。

Vaultをセットアップする前に、必要な依存ツールがインストールされ、
正しいバージョンであることを確認する。

終了コード:
    0 - すべての必須ツールが確認できた
    1 - 必須ツールの不足、またはバージョン不一致（利用者側で対処可能）
    2 - 想定外のエラー
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

REQUIRED_PYTHON_VERSION = (3, 11, 9)


class ToolCheck:
    def __init__(self, name: str, command: list[str], required: bool, note: str = ""):
        self.name = name
        self.command = command
        self.required = required
        self.note = note


def check_python_version() -> tuple[bool, str]:
    actual = sys.version_info[:3]
    if actual == REQUIRED_PYTHON_VERSION:
        return True, f"Python {'.'.join(map(str, actual))}"
    expected = ".".join(map(str, REQUIRED_PYTHON_VERSION))
    return False, f"Python {'.'.join(map(str, actual))}（要求バージョン: {expected} 厳密一致）"


def check_tool(tool: ToolCheck) -> tuple[bool, str]:
    path = shutil.which(tool.command[0])
    if path is None:
        return False, f"{tool.name} が見つかりません（PATHに存在しません）"
    try:
        result = subprocess.run(
            tool.command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{tool.name} の実行に失敗しました: {exc}"
    version_line = (result.stdout or result.stderr or "").strip().splitlines()
    version_text = version_line[0] if version_line else "(バージョン不明)"
    return True, f"{tool.name}: {version_text}（{path}）"


def build_tool_checks() -> list[ToolCheck]:
    # docs/requirements.md 6節 Q7 で確定した依存ツール一覧。
    return [
        ToolCheck("Git", ["git", "--version"], required=True),
        ToolCheck("uv", ["uv", "--version"], required=True, note="主パッケージ管理ツール"),
        ToolCheck("pip", [sys.executable, "-m", "pip", "--version"], required=True, note="フォールバック"),
        ToolCheck("Node.js", ["node", "--version"], required=False, note="必要に応じて"),
    ]


def run_checks() -> int:
    has_error = False
    ok, message = check_python_version()
    print(f"[{'OK' if ok else 'NG'}] {message}")
    if not ok:
        has_error = True

    for tool in build_tool_checks():
        ok, message = check_tool(tool)
        label = "OK" if ok else ("NG" if tool.required else "警告")
        print(f"[{label}] {message}")
        if not ok and tool.required:
            has_error = True

    if has_error:
        print("必須ツールの不足、またはバージョン不一致があります。上記を解消してください。", file=sys.stderr)
        return 1
    print("すべての必須ツールを確認できました。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_env.py",
        description="第二の脳（Second Brain）のセットアップに必要な環境を確認する。",
    )
    parser.parse_args(argv)

    try:
        return run_checks()
    except Exception as exc:  # noqa: BLE001 - CLIの最終防衛ライン
        print(f"想定外のエラーが発生しました: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
