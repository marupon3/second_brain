#!/usr/bin/env bash
# CLAUDE.md 4節: obsidian_vault/raw/配下のファイルはAIが編集・削除してはならない。
# Edit/Write/NotebookEditツールがraw/配下を対象にした場合はブロックする。
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

path=$(printf '%s' "$input" | "$PY" -c "
import json, sys
try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
ti = data.get('tool_input') or {}
print(ti.get('file_path') or ti.get('notebook_path') or '')
")

if [[ -z "$path" ]]; then
  exit 0
fi

if [[ "$path" == *"obsidian_vault/raw/"* ]]; then
  "$PY" -c "
import json
reason = 'CLAUDE.mdの禁止事項により、obsidian_vault/raw/配下のファイルはAIが編集・削除できません（不変の原文ソースのため人間のみが書き込みます）。内容を反映したい場合は、/ingestでwiki/へ要約するか、変更が必要な理由をユーザーに確認してください。'
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': reason}}, ensure_ascii=False))
"
  exit 0
fi

exit 0
