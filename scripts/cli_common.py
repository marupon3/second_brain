"""scripts/配下のコマンドが共通して使う小さなユーティリティ。

各スクリプトが個別に持っていた以下の処理をここへ集約する。挙動は集約前と同一。

- テキスト入出力のエンコーディング定数（`CLAUDE.md` 3節: すべてUTF-8で保存する）
- 標準出力・標準エラーのUTF-8設定（Windows既定のコードページ対策）
- 想定外の例外を終了コード2に落とすCLIの最終防衛ライン

`scripts/`はパッケージではなく単体スクリプト群のため、`python scripts/<名前>.py`
として実行したときにスクリプト自身のディレクトリがsys.pathへ入ることを前提に、
`from cli_common import ...`の形で読み込む（`migrate_vault.py`が
`convert_onenote_note.py`を読み込んでいるのと同じ方式）。
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

ENCODING = "utf-8"


def configure_stdio_encoding() -> None:
    """標準出力・標準エラーがUTF-8でなければ再設定する。

    日本語のメッセージを出力するため、各コマンドのエントリポイントで最初に呼ぶ。
    """
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != ENCODING:
        sys.stdout.reconfigure(encoding=ENCODING)
        sys.stderr.reconfigure(encoding=ENCODING)


def run_cli(run: Callable[[], int]) -> int:
    """コマンド本体を実行し、想定外の例外を終了コード2に落とす（最終防衛ライン）。"""
    try:
        return run()
    except Exception as exc:  # noqa: BLE001 - CLIの最終防衛ライン
        print(f"想定外のエラーが発生しました: {exc}", file=sys.stderr)
        return 2


def write_text(path: Path, text: str) -> None:
    """親ディレクトリを作成したうえで、UTF-8を明示してテキストを書き込む。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=ENCODING)
