"""Vaultディレクトリ構造生成コマンド。

docs/basic-design.md 2節のディレクトリツリーに沿って、Vaultの構造を生成する。
既存のファイル・ディレクトリは上書きしない（非破壊的操作のため確認プロンプトは不要）。

終了コード:
    0 - 正常終了
    1 - 指定した対象ディレクトリが不正（利用者側で対処可能）
    2 - 想定外のエラー
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# docs/basic-design.md 2節（v1.1, weekly/追加済み。ユーザーが直接情報を追加する
# raw/daily/projects/areas/resources/templatesはobsidian_vault/配下に集約）に対応。
DIRECTORIES = [
    "obsidian_vault/raw/articles",
    "obsidian_vault/raw/notes",
    "obsidian_vault/raw/pdfs",
    "obsidian_vault/raw/personal",
    "wiki",
    "obsidian_vault/daily",
    "weekly",
    "obsidian_vault/projects",
    "obsidian_vault/areas",
    "obsidian_vault/resources",
    "obsidian_vault/private",  # ローカル専用（.gitignoreで除外、リモートには含めない）
    "obsidian_vault/templates",
    ".claude/skills/daily",
    ".claude/skills/weekly",
    ".claude/skills/ingest",
    ".claude/skills/lint",
    ".claude/skills/research",
    "scripts",
]

WIKI_PLACEHOLDERS: dict[str, str] = {
    "wiki/index.md": "---\ntitle: Index\n---\n\n# Index\n\n（まだページがありません）\n",
    "wiki/log.md": "---\ntitle: Log\n---\n\n# Log\n\n（まだ記録がありません）\n",
    "wiki/overview.md": "---\ntitle: Overview\n---\n\n# Overview\n\n（まだ記述がありません）\n",
}


def create_directories(root: Path) -> list[Path]:
    created: list[Path] = []
    for rel in DIRECTORIES:
        target = root / rel
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            created.append(target)
    return created


def create_wiki_placeholders(root: Path) -> list[Path]:
    created: list[Path] = []
    for rel, content in WIKI_PLACEHOLDERS.items():
        target = root / rel
        if not target.exists():
            target.write_text(content, encoding="utf-8")
            created.append(target)
    return created


def run_setup(target: Path) -> int:
    if target.exists() and not target.is_dir():
        print(f"対象パスがディレクトリではありません: {target}", file=sys.stderr)
        return 1

    target.mkdir(parents=True, exist_ok=True)

    created_dirs = create_directories(target)
    created_files = create_wiki_placeholders(target)

    for path in created_dirs:
        print(f"作成: {path}")
    for path in created_files:
        print(f"作成: {path}")

    if not created_dirs and not created_files:
        print("すべてのディレクトリ・ファイルは既に存在します。変更はありません。")
    else:
        print(f"Vaultディレクトリ構造の生成が完了しました（対象: {target}）。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="setup.py",
        description="第二の脳（Second Brain）のVaultディレクトリ構造を生成する（非破壊的、既存ファイルは上書きしない）。",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Vaultを生成する対象ディレクトリ（省略時はカレントディレクトリ）",
    )
    args = parser.parse_args(argv)

    try:
        target = Path(args.target).resolve()
        return run_setup(target)
    except OSError as exc:
        print(f"ファイル操作でエラーが発生しました: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - CLIの最終防衛ライン
        print(f"想定外のエラーが発生しました: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
