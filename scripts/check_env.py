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
from dataclasses import dataclass

from cli_common import configure_stdio_encoding, run_cli

REQUIRED_PYTHON_VERSION = (3, 11, 9)


@dataclass(frozen=True)
class ToolCheck:
    """確認対象のツール1件。`command`はバージョン確認用のコマンド列。"""

    name: str
    command: list[str]
    required: bool


def _format_version(version: tuple[int, ...]) -> str:
    return ".".join(map(str, version))


def check_python_version() -> tuple[bool, str]:
    actual = sys.version_info[:3]
    actual_text = _format_version(actual)
    if actual == REQUIRED_PYTHON_VERSION:
        return True, f"Python {actual_text}"
    expected_text = _format_version(REQUIRED_PYTHON_VERSION)
    return False, f"Python {actual_text}（要求バージョン: {expected_text} 厳密一致）"


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
        # uv: 主パッケージ管理ツール
        ToolCheck("uv", ["uv", "--version"], required=True),
        # pip: uvが使えない場合のフォールバック
        ToolCheck("pip", [sys.executable, "-m", "pip", "--version"], required=True),
        # Node.js: 必要に応じて利用するため必須ではない
        ToolCheck("Node.js", ["node", "--version"], required=False),
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
        print(
            "必須ツールの不足、またはバージョン不一致があります。上記を解消してください。",
            file=sys.stderr,
        )
        return 1
    print("すべての必須ツールを確認できました。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_env.py",
        description="第二の脳（Second Brain）のセットアップに必要な環境を確認する。",
    )
    parser.parse_args(argv)

    return run_cli(run_checks)


if __name__ == "__main__":
    configure_stdio_encoding()
    sys.exit(main())
