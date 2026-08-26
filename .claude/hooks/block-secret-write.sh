#!/usr/bin/env bash
# CLAUDE.md 4節: APIキー等の秘密情報をMarkdownファイルやコード中に直接書き込まない。
# Edit/Write/NotebookEditで書き込まれる内容にAPIキーらしきパターンが含まれる場合はブロックする。
# 過去にobsidian_vault/raw/内の画像へGoogle APIキーが写り込みpush済みだった実インシデントがあるため、
# 文言のみの禁止（CLAUDE.md 4節）に加えて機構的な検知を行う。
set -euo pipefail

input=$(cat)
# jqはWindows環境に標準で入っていないため、CLAUDE.md 1節で前提としているPythonで
# JSON入出力を行う。Windows環境では`python3`という名前のコマンドが無いことが多く
# `python`のみ存在するため、両方を試して見つかった方を使う（見つからなければHookは
# 機能しないが、Hook自体のエラーで正規の操作まで止めないよう安全側に倒す）。
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  exit 0
fi

printf '%s' "$input" | "$PY" -c "
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)

ti = data.get('tool_input') or {}
# Write: content / Edit: new_string / NotebookEdit: new_source
text = ti.get('content') or ti.get('new_string') or ti.get('new_source') or ''

patterns = [
    ('Google API Key', r'AIza[0-9A-Za-z_-]{35}'),
    ('Anthropic API Key', r'sk-ant-[A-Za-z0-9_-]{20,}'),
    ('GitHub Token', r'gh[pousr]_[A-Za-z0-9]{36}'),
    ('GitHub Fine-grained PAT', r'github_pat_[A-Za-z0-9_]{22,}'),
    ('AWS Access Key ID', r'AKIA[0-9A-Z]{16}'),
    ('OpenAI-style API Key', r'sk-[A-Za-z0-9]{20,}'),
]

label = None
for name, pattern in patterns:
    if re.search(pattern, text):
        label = name
        break

if label is None:
    sys.exit(0)

reason = (
    'CLAUDE.mdの禁止事項により、APIキー等の秘密情報をMarkdownファイルやコード中に直接書き込めません'
    f'（{label}らしきパターンを検知）。.envまたは環境変数を使うか、誤検知であればユーザーに確認してください。'
)
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': reason}}, ensure_ascii=False))
"

exit 0
