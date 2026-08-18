"""OneNoteからMarkdown変換済みのファイルを、obsidian_vault/raw/notes/の
YAML frontmatterテンプレート形式（メモ:/source:）に変換して移行するスクリプト。

設計方針・前提:
- obsidian_vault/raw/ は CLAUDE.md 上「人間のみが書き込む不変ソース」と定義されている。
  本スクリプトはAIが自律的にraw/を書き換えるものではなく、ユーザー自身がOneNote由来の
  個人メモをVaultに投入する作業を補助するツールという位置づけ。既存ファイルは上書きしない。
- 既定はドライラン（変換結果を標準出力に表示するのみ）。実際にファイルを書き込むには
  明示的に --apply を指定する（CLAUDE.md 4節「破壊的操作は確認を取る」に準拠した安全策）。
- コード領域の行復元は、OneNote側の改行位置に依存せず、括弧の深さとast.parseによる
  構文的な妥当性判定で行う（見た目の推測に頼らない）。ただし元テキストのインデントが
  OneNote側で失われている場合があり、その点は変換結果の先頭に注記コメントを付けて
  必ず目視確認を促す（不確実な箇所を無断で断定しない方針）。

使い方:
    python scripts/convert_onenote_note.py <入力ファイルまたはフォルダ> [--apply]
        [--output obsidian_vault/raw/notes] [--force]

例:
    python scripts/convert_onenote_note.py "C:\\Users\\marupon\\Downloads\\onenote_export" --apply
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from cli_common import ENCODING, write_text

# OneNote/変換ツール由来のMarkdownエスケープ（アンダースコア・アスタリスク）
_ESCAPE_PATTERN = re.compile(r"\\([_*])")

# 続き（前の断片の続きである可能性が高い）とみなす行頭パターン。
# else/elif/except/finally や閉じ括弧はそれ自体が新しい論理行の先頭になり得るため、
# ここには含めない（誤って前の行に結合してしまうバグの原因になる）。
_CONTINUATION_PREFIXES = ("as ",)

# OneNote由来のノーブレークスペース（\xa0）。インデント量の計測前に半角スペースへ正規化する。
_NBSP = "\xa0"

_DATE_LINE_PATTERN = re.compile(r"^(\d{4})年(\d{1,2})月(\d{1,2})日$")
_TIME_LINE_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")
_FILENAME_DATE_PATTERN = re.compile(r"^(\d{4})(\d{2})(\d{2})[\s_-]*(.*)$")
_ONENOTE_FOOTER_PATTERN = re.compile(r"^OneNote\s*で作成されました。?$")
_HEADING_LINE_PATTERN = re.compile(r"^#([^\s#].*)$")
_CODE_START_PATTERN = re.compile(r"^\s*(import\s|from\s.+import|def\s|class\s)")

REVIEW_NOTE = (
    "<!-- 変換時の注記: OneNote由来の改行を括弧深さ/構文解析で自動復元しました。"
    "インデントはOneNote側で失われている場合があり保証されません。"
    "実行前に必ず目視確認してください（要確認）。 -->"
)


@dataclass
class ConvertedNote:
    title: str
    date: str | None
    time: str | None
    body_lines: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def unescape_markdown(text: str) -> str:
    """OneNote変換で付与された \\_ \\* のバックスラッシュエスケープを解除する。"""
    return _ESCAPE_PATTERN.sub(r"\1", text)


def _bracket_delta(fragment: str) -> int:
    opens = fragment.count("(") + fragment.count("[") + fragment.count("{")
    closes = fragment.count(")") + fragment.count("]") + fragment.count("}")
    return opens - closes


def _split_fragments(raw_lines: list[str]) -> list[tuple[int, str]]:
    """OneNote由来の行を (インデント量, 本文) の断片リストへ変換する。

    OneNoteのMarkdown書き出しでは、1つの元の行が複数の断片に分かれ、かつ
    インデント（\\xa0の連続）だけの断片が本文と別の行に分離されることがある
    （例: 空白のみの行の直後に、インデント無しの本文行が続く）。
    その場合はインデントのみの断片を「次の本文断片のインデント」として保持する。
    """
    fragments: list[tuple[int, str]] = []
    pending_indent: int | None = None
    for raw in raw_lines:
        normalized = raw.replace(_NBSP, " ")
        if normalized.strip() == "":
            if normalized != "" and normalized.strip(" ") == "":
                # 空白（\xa0起源）のみの行はインデント量として記憶しておく。
                # 通常の行は「\xa0の連続 + 半角スペース1文字 + 本文」の形で
                # 出現するため、本文を伴わないこの行にも同じ+1を適用して
                # インデント幅の基準を揃える。
                pending_indent = len(normalized) + 1
            continue
        content = normalized.lstrip(" ")
        indent_len = len(normalized) - len(content)
        text = unescape_markdown(content.rstrip())
        if not text:
            continue
        if indent_len == 0 and pending_indent is not None:
            indent_len = pending_indent
        pending_indent = None
        fragments.append((indent_len, text))
    return fragments


def reconstruct_code_lines(raw_lines: list[str]) -> tuple[list[str], list[str]]:
    """OneNoteの改行でバラバラになったコード断片を、括弧の深さと構文解析で
    論理行単位に復元する。インデントは各論理行の最初の断片が持つ先頭空白量
    （OneNote側で保持されている\\xa0の連続）をそのまま採用する。
    戻り値は (復元済み行のリスト, 警告メッセージのリスト)。
    """
    fragments = _split_fragments(raw_lines)

    lines: list[str] = []
    warnings: list[str] = []
    buffer = ""
    buffer_indent = 0
    depth = 0
    i = 0
    n = len(fragments)
    while i < n:
        indent_len, frag = fragments[i]
        if buffer:
            buffer = f"{buffer} {frag}"
        else:
            buffer = frag
            buffer_indent = indent_len
        depth += _bracket_delta(frag)
        i += 1

        if depth > 0:
            continue  # 括弧が閉じるまでは必ず継続行として扱う

        content = buffer.rstrip()

        if content.endswith(":"):
            lines.append(" " * buffer_indent + content)
            buffer = ""
            continue

        next_frag = fragments[i][1] if i < n else ""
        if next_frag.startswith(_CONTINUATION_PREFIXES):
            continue  # 次の断片が続き語（as等）で始まる場合は結合を継続

        try:
            ast.parse(content)  # インデントを含めず構文的な完結性のみ検証する
            lines.append(" " * buffer_indent + content)
            buffer = ""
        except SyntaxError:
            continue  # 単独では構文として不完全なため続きを取り込む

    if buffer:
        warnings.append(
            f"末尾の断片が構文的に完結しませんでした（要確認）: {buffer!r}"
        )
        lines.append(" " * buffer_indent + buffer)

    # 復元結果全体が構文的に妥当か最終検証する（妥当性の担保であり、断定はしない）
    try:
        ast.parse("\n".join(lines))
    except SyntaxError as exc:
        warnings.append(
            f"復元後のコード全体がPythonとして解析できませんでした（要確認）: {exc}"
        )

    return lines, warnings


def extract_title_and_date_from_filename(path: Path) -> tuple[str, str | None]:
    stem = path.stem
    m = _FILENAME_DATE_PATTERN.match(stem)
    if m:
        year, month, day, rest = m.groups()
        date = f"{year}-{month}-{day}"
        title = rest.strip() or stem
        return title, date
    return stem, None


def _skip_blank_lines(lines: list[str], idx: int) -> int:
    """`idx`から続く空行を読み飛ばし、次に内容のある行の位置を返す。"""
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    return idx


def _extract_title(lines: list[str], idx: int, fallback_title: str) -> tuple[str, int]:
    """先頭行からタイトルを取り出し、(タイトル, 次の走査位置)を返す。

    1行目はタイトル行（ファイル名と重複するケースが多い）。ただし
    「20240806」のように日付のみが1行目に単独で置かれ、実際のタイトルが
    次の行に分かれているケースがあるため、その場合は次の行もタイトルとして拾う。
    """
    if not (idx < len(lines) and lines[idx].strip()):
        return fallback_title, idx

    first_line = lines[idx].strip()
    m = _FILENAME_DATE_PATTERN.match(first_line)
    if not m:
        return unescape_markdown(first_line), idx + 1

    _, _, _, rest = m.groups()
    title = unescape_markdown(rest.strip())
    idx += 1
    if not title and idx < len(lines) and lines[idx].strip():
        next_line = lines[idx].strip()
        if not (
            _DATE_LINE_PATTERN.match(next_line)
            or _TIME_LINE_PATTERN.match(next_line)
            or _FILENAME_DATE_PATTERN.match(next_line)
        ):
            title = unescape_markdown(next_line)
            idx += 1
    if not title:
        title = unescape_markdown(first_line)
    return title, idx


def _extract_date_and_time(
    lines: list[str], idx: int, date: str | None
) -> tuple[str | None, str | None, int]:
    """タイトルに続く数行から日付行・時刻行を拾う。

    行から日付が見つかった場合は、引数で渡されたファイル名由来の日付より優先する。
    戻り値は (日付, 時刻, 次の走査位置)。
    """
    time_value: str | None = None
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped == "":
            idx += 1
            continue
        date_match = _DATE_LINE_PATTERN.match(stripped)
        time_match = _TIME_LINE_PATTERN.match(stripped)
        if date_match:
            y, mo, d = date_match.groups()
            date = f"{y}-{int(mo):02d}-{int(d):02d}"
            idx += 1
            continue
        if time_match:
            time_value = stripped
            idx += 1
            continue
        break
    return date, time_value, idx


def _strip_onenote_footer(body_source_lines: list[str]) -> list[str]:
    """末尾のOneNoteフッターと、それに続く空行を除去する。"""
    trimmed = list(body_source_lines)
    while trimmed and (
        trimmed[-1].strip() == "" or _ONENOTE_FOOTER_PATTERN.match(trimmed[-1].strip())
    ):
        trimmed.pop()
    return trimmed


def _split_prose_and_code(body_source_lines: list[str]) -> tuple[list[str], list[str]]:
    """本文を見出し・箇条書き領域（prose）とコード領域に分離する。

    コード領域は最初にimport/def/class等が現れた行以降の全てとし、
    復元は`reconstruct_code_lines`に委ねるため生の行のまま返す。
    """
    prose_lines: list[str] = []
    code_raw_lines: list[str] = []
    in_code = False
    for line in body_source_lines:
        stripped = line.strip()
        if not in_code and _CODE_START_PATTERN.match(stripped):
            in_code = True
        if in_code:
            code_raw_lines.append(line)
            continue
        if stripped == "":
            continue
        heading_match = _HEADING_LINE_PATTERN.match(stripped)
        if heading_match:
            if prose_lines and prose_lines[-1] != "":
                prose_lines.append("")
            prose_lines.append(f"## {heading_match.group(1)}")
            prose_lines.append("")
        else:
            prose_lines.append(unescape_markdown(stripped))

    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    return prose_lines, code_raw_lines


def _build_body_lines(
    title: str, prose_lines: list[str], code_raw_lines: list[str]
) -> tuple[list[str], list[str]]:
    """タイトル・本文・コードブロックを組み立てる。戻り値は (本文行, 警告)。"""
    body_lines: list[str] = [f"# {title}", ""]
    if prose_lines:
        body_lines.extend(prose_lines)
        body_lines.append("")

    warnings: list[str] = []
    if code_raw_lines:
        code_lines, code_warnings = reconstruct_code_lines(code_raw_lines)
        warnings.extend(code_warnings)
        body_lines.append(REVIEW_NOTE)
        body_lines.append("")
        body_lines.append("```python")
        body_lines.extend(code_lines)
        body_lines.append("```")
        body_lines.append("")

    return body_lines, warnings


def parse_onenote_markdown(path: Path, raw_text: str) -> ConvertedNote:
    lines = raw_text.splitlines()
    fallback_title, filename_date = extract_title_and_date_from_filename(path)

    idx = _skip_blank_lines(lines, 0)
    title, idx = _extract_title(lines, idx, fallback_title)
    date, time_value, idx = _extract_date_and_time(lines, idx, filename_date)

    body_source_lines = _strip_onenote_footer(lines[idx:])
    prose_lines, code_raw_lines = _split_prose_and_code(body_source_lines)
    body_lines, warnings = _build_body_lines(title, prose_lines, code_raw_lines)

    if date is None:
        warnings.append("日付を特定できませんでした（要確認・手動で補記してください）")

    return ConvertedNote(
        title=title,
        date=date,
        time=time_value,
        body_lines=body_lines,
        warnings=warnings,
    )


def render_note(note: ConvertedNote) -> str:
    frontmatter = ["---"]
    frontmatter.append(f"メモ: {note.date if note.date else '要確認'}")
    frontmatter.append("source: OneNote")
    if note.time:
        frontmatter.append(f"作成時刻: {note.time}")
    frontmatter.append("---")
    frontmatter.append("")
    return "\n".join(frontmatter + note.body_lines).rstrip() + "\n"


def output_filename(note: ConvertedNote, original: Path) -> str:
    if note.date:
        return f"{note.date} {note.title}.md"
    return original.name


def convert_file(path: Path) -> tuple[ConvertedNote, str, str]:
    raw_text = path.read_text(encoding=ENCODING)
    note = parse_onenote_markdown(path, raw_text)
    rendered = render_note(note)
    out_name = output_filename(note, path)
    return note, rendered, out_name


def collect_input_files(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        return sorted(input_path.glob("*.md"))
    if input_path.is_file():
        return [input_path]
    raise FileNotFoundError(f"入力パスが見つかりません: {input_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="OneNote変換済みMarkdownをobsidian_vault/raw/notes/形式に変換する"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="OneNote変換済み.mdファイル、またはそれらを含むフォルダ",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("obsidian_vault/raw/notes"),
        help="出力先フォルダ（既定: obsidian_vault/raw/notes）",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="実際にファイルを書き込む（未指定時はドライランで内容のみ表示）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="出力先に同名ファイルが既に存在していても上書きする",
    )
    args = parser.parse_args()

    try:
        input_files = collect_input_files(args.input)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if not input_files:
        print("[INFO] 対象となる.mdファイルが見つかりませんでした。")
        return 0

    exit_code = 0
    for path in input_files:
        try:
            note, rendered, out_name = convert_file(path)
        except Exception as exc:  # noqa: BLE001 - 1件の失敗で全体を止めない
            print(f"[ERROR] {path.name}: 変換に失敗しました: {exc}", file=sys.stderr)
            exit_code = 1
            continue

        out_path = args.output / out_name
        print(f"=== {path.name} -> {out_path} ===")
        if note.warnings:
            for w in note.warnings:
                print(f"[WARN] {w}")

        if not args.apply:
            print(rendered)
            print("[INFO] ドライラン実行中のため書き込みは行っていません（--apply で書き込み）。")
            continue

        if out_path.exists() and not args.force:
            print(f"[SKIP] 既に存在するため上書きしません（--force で上書き可）: {out_path}")
            continue

        write_text(out_path, rendered)
        print(f"[OK] 書き込みました: {out_path}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
