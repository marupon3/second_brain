"""既存の個人用Obsidian Vault（OneNoteから移行済み）から、second_brainの
obsidian_vault/raw/ 配下（articles/notes/pdfs/personal）へノートを一括移行するスクリプト。

前提・設計方針:
- convert_onenote_note.py のfrontmatter変換・コード復元ロジックをそのまま再利用する。
- 移行元Vaultのトップレベルフォルダ名（PSQL, WEBから, 薬 等）から、raw/配下のカテゴリへ
  自動でマッピングする（CATEGORY_MAP）。マッピング表に無いフォルダはnotesに分類したうえで
  未定義である旨を警告として出力する（無断で断定しない）。
- 「削除されたページ」フォルダ、および読み取り不能なフォルダ（OneDriveのオンデマンド
  ファイル未ダウンロード等でI/Oエラーになるもの）は対象から除外し、除外一覧を報告する。
- ノート本文中の画像参照（Markdown形式 ![](path) およびWiki形式 ![[name]]）を検出し、
  実体ファイルを移行先の同じ相対パスへコピーする。リンクの文字列自体は書き換えない
  （コピー先の相対構造をリンクと一致させることで、書き換え無しにリンクを保持する）。
- 既定はドライラン。書き込みには --apply が必要（CLAUDE.md 4節に準拠した安全策）。

使い方:
    python scripts/migrate_vault.py <移行元Vaultフォルダ> [<移行元Vaultフォルダ2> ...]
        [--apply] [--force]

例:
    python scripts/migrate_vault.py "C:\\Users\\marupon\\Documents\\Obsidian Vault\\仕事用" \\
        "C:\\Users\\marupon\\Documents\\Obsidian Vault\\情報収集" --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from cli_common import ENCODING, write_text
from convert_onenote_note import output_filename, parse_onenote_markdown, render_note

# トップレベルフォルダ名 -> obsidian_vault/raw/ 配下のカテゴリ
CATEGORY_MAP: dict[str, str] = {
    # 仕事用
    "Android": "notes",
    "claude Code": "notes",
    "PSQL": "notes",
    "Python": "notes",
    "Tips": "notes",
    "仕事関係": "notes",
    "小児用量アプリ": "notes",
    "生成AI": "notes",
    "高速検索": "notes",
    # 情報収集
    "Linux": "notes",
    "Mac": "notes",
    "Ubuntu_python": "notes",
    "Windows": "notes",
    "薬": "notes",
    "写真": "notes",
    "図書館で借りた本": "notes",
    "書籍から": "notes",
    "WEBから": "articles",
    "WEBから 2": "articles",
    "人工知能ブーム": "articles",
    "日経ビジネス": "articles",
    "その他": "personal",
}

# 常に除外するフォルダ名（木の深さを問わず一致したら除外）
EXCLUDE_DIR_NAMES = {"削除されたページ"}

_MD_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_WIKI_IMAGE_PATTERN = re.compile(r"!\[\[([^\]]+)\]\]")

# 1件のノートを処理した結果。
Outcome = Literal["ok", "skip", "error"]


@dataclass
class MigrationCounts:
    """移行結果の集計（成功・スキップ・エラーの件数）。"""

    ok: int = 0
    skip: int = 0
    error: int = 0

    def record(self, outcome: Outcome) -> None:
        if outcome == "ok":
            self.ok += 1
        elif outcome == "skip":
            self.skip += 1
        else:
            self.error += 1

    def merge(self, other: MigrationCounts) -> None:
        self.ok += other.ok
        self.skip += other.skip
        self.error += other.error


def find_markdown_files(root: Path) -> tuple[list[Path], list[str]]:
    """root配下の.mdファイルを再帰的に収集する。EXCLUDE_DIR_NAMESと読み取り不能な
    フォルダはスキップし、スキップ理由を報告用文字列のリストとして返す。
    """
    md_files: list[Path] = []
    skipped: list[str] = []

    def walk(dir_path: Path) -> None:
        try:
            entries = sorted(dir_path.iterdir())
        except OSError as exc:
            skipped.append(f"[SKIP-IO] 読み取り不能のため除外: {dir_path} ({exc})")
            return
        for entry in entries:
            if entry.is_dir():
                if entry.name in EXCLUDE_DIR_NAMES:
                    skipped.append(f"[SKIP] 除外フォルダのため対象外: {entry}")
                    continue
                walk(entry)
            elif entry.suffix.lower() == ".md":
                md_files.append(entry)

    walk(root)
    return md_files, skipped


def resolve_local_image_paths(rendered_text: str) -> list[str]:
    """本文中のローカル画像参照（http(s)を除く）を抽出する。"""
    paths: list[str] = []
    for m in _MD_IMAGE_PATTERN.finditer(rendered_text):
        p = m.group(1).strip()
        if not p.startswith(("http://", "https://")):
            paths.append(p)
    for m in _WIKI_IMAGE_PATTERN.finditer(rendered_text):
        paths.append(m.group(1).strip())
    return paths


def dedupe_dest_path(base: Path, used_paths: set[Path], force: bool) -> Path:
    """移行先パスの衝突を回避する。

    同名タイトルの別ページ（OneNoteの複製ページ等）が同じ出力ファイル名に
    なるケースがあるため、今回の実行内で既に使用したパスと衝突する場合は
    「 (2)」「 (3)」...を付けて別ファイルとして保存する（黙って上書き・破棄しない）。
    --forceは「前回実行で書き込み済みの既存ファイルを上書きしてよい」という
    意味であり、今回の実行内での別ソース同士の衝突には適用しない。
    """
    if base not in used_paths and (force or not base.exists()):
        return base
    n = 2
    while True:
        candidate = base.with_name(f"{base.stem} ({n}){base.suffix}")
        if candidate not in used_paths and not candidate.exists():
            return candidate
        n += 1


def copy_images(src_dir: Path, dest_dir: Path, image_paths: list[str]) -> None:
    """本文から検出した画像を、リンクと同じ相対パスで移行先へコピーする。

    リンク文字列自体は書き換えず、相対構造を一致させることでリンクを保持する。
    """
    for img_rel in image_paths:
        src_img = (src_dir / img_rel).resolve()
        if not src_img.is_file():
            print(f"  [WARN] 画像が見つかりません（要確認）: {img_rel}")
            continue
        dest_img = dest_dir / img_rel
        try:
            dest_img.parent.mkdir(parents=True, exist_ok=True)
            dest_img.write_bytes(src_img.read_bytes())
        except OSError as exc:
            print(f"  [WARN] 画像のコピーに失敗しました（要確認）: {img_rel} ({exc})")


def migrate_note(
    md_path: Path,
    dest_dir: Path,
    apply: bool,
    force: bool,
    used_paths: set[Path],
) -> Outcome:
    """1件のノートを読み取り・変換し、必要なら書き込む。1件の失敗で全体を止めない。"""
    try:
        raw_text = md_path.read_text(encoding=ENCODING)
    except OSError as exc:
        print(f"[SKIP-IO] 読み取り不能のため除外: {md_path} ({exc})")
        return "skip"
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {md_path}: 読み込みに失敗しました: {exc}", file=sys.stderr)
        return "error"

    try:
        note = parse_onenote_markdown(md_path, raw_text)
        rendered = render_note(note)
        out_name = output_filename(note, md_path)
    except Exception as exc:  # noqa: BLE001 - 1件の失敗で全体を止めない
        print(f"[ERROR] {md_path}: 変換に失敗しました: {exc}", file=sys.stderr)
        return "error"

    base_dest_path = dest_dir / out_name
    dest_path = dedupe_dest_path(base_dest_path, used_paths, force)
    used_paths.add(dest_path)  # ドライランでも計画上は使用済みとして扱う
    if dest_path != base_dest_path:
        print(f"{md_path} -> {dest_path}  [別ソースと同名のため退避（要確認）]")
    else:
        print(f"{md_path} -> {dest_path}")
    for w in note.warnings:
        print(f"  [WARN] {w}")

    image_paths = resolve_local_image_paths(rendered)

    if not apply:
        return "skip"

    if base_dest_path.exists() and dest_path == base_dest_path and not force:
        print(f"  [SKIP] 既に存在するため上書きしません（--force で上書き可）: {dest_path}")
        return "skip"

    write_text(dest_path, rendered)
    copy_images(md_path.parent, dest_dir, image_paths)

    print(f"  [OK] 書き込みました: {dest_path}")
    return "ok"


def migrate_root(
    root: Path,
    vault_raw: Path,
    apply: bool,
    force: bool,
    used_paths: set[Path],
) -> MigrationCounts:
    """1つの移行元Vaultフォルダを処理し、件数の集計を返す。"""
    print(f"\n#### 移行元: {root} ####")
    counts = MigrationCounts()

    try:
        top_level_dirs = sorted(p for p in root.iterdir() if p.is_dir())
    except OSError as exc:
        print(f"[ERROR] トップレベルの読み取りに失敗しました: {root} ({exc})", file=sys.stderr)
        counts.error += 1
        return counts

    for top_dir in top_level_dirs:
        if top_dir.name in EXCLUDE_DIR_NAMES:
            print(f"[SKIP] 除外フォルダのため対象外: {top_dir}")
            counts.skip += 1
            continue

        category = CATEGORY_MAP.get(top_dir.name)
        if category is None:
            category = "notes"
            print(f"[WARN] '{top_dir.name}' はカテゴリ未定義のため notes に分類します（要確認）")

        md_files, skipped_msgs = find_markdown_files(top_dir)
        for msg in skipped_msgs:
            print(msg)
            counts.skip += 1

        for md_path in md_files:
            rel_dir = md_path.parent.relative_to(root)  # 例: PSQL または PSQL/サブフォルダ
            dest_dir = vault_raw / category / rel_dir
            counts.record(migrate_note(md_path, dest_dir, apply, force, used_paths))

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="既存Obsidian Vaultからsecond_brainのobsidian_vault/raw/へ一括移行する"
    )
    parser.add_argument("roots", type=Path, nargs="+", help="移行元Vaultフォルダ（複数指定可）")
    parser.add_argument(
        "--vault-raw",
        type=Path,
        default=Path("obsidian_vault/raw"),
        help="移行先のraw/フォルダ（既定: obsidian_vault/raw）",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="実際にファイルを書き込む（未指定時はドライランで一覧のみ表示）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="移行先に同名ファイルが既に存在していても上書きする",
    )
    args = parser.parse_args()

    totals = MigrationCounts()
    used_paths: set[Path] = set()
    for root in args.roots:
        if not root.is_dir():
            print(f"[ERROR] 移行元フォルダが見つかりません: {root}", file=sys.stderr)
            totals.error += 1
            continue
        totals.merge(migrate_root(root, args.vault_raw, args.apply, args.force, used_paths))

    print(f"\n#### 集計: 成功 {totals.ok} / スキップ {totals.skip} / エラー {totals.error} ####")
    if not args.apply:
        print("[INFO] ドライラン実行中のため書き込みは行っていません（--apply で書き込み）。")

    return 1 if totals.error else 0


if __name__ == "__main__":
    raise SystemExit(main())
