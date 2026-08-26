#!/usr/bin/env bash
# CLAUDE.md 4節: obsidian_vault/raw/配下のファイルはAIが編集・削除してはならない。
# Bash経由でraw/配下を対象にした破壊的操作（削除・上書き・書き換え）をブロックする。
# 単純な文字列grepだとクォート内の文字列（コミットメッセージ・JSON等）に含まれる
# 「rm」「>」等の文字列にも誤反応するため、shlexでシェルトークンとして正しく分割し、
# クォートされた文字列は1トークンとして扱った上で、コマンドの先頭トークン（動詞）を判定する。
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

command=$(printf '%s' "$input" | "$PY" -c "
import json, sys
try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
ti = data.get('tool_input') or {}
print(ti.get('command') or '')
")

if [[ -z "$command" ]]; then
  exit 0
fi

blocked=$("$PY" - "$command" <<'PYEOF'
import shlex
import sys

command = sys.argv[1]

try:
    tokens = shlex.split(command, posix=True)
except ValueError:
    # クォートの対応が取れない等でパースできない場合は安全側に倒して素通しする
    tokens = []

segments = []
current = []
for tok in tokens:
    if tok in (';', '&&', '||', '|'):
        segments.append(current)
        current = []
    else:
        current.append(tok)
segments.append(current)

danger_verbs = {'rm', 'mv', 'tee', 'dd', 'truncate'}


def targets_raw(seg):
    return any('obsidian_vault/raw/' in t for t in seg)


blocked = False
for seg in segments:
    if not seg or not targets_raw(seg):
        continue
    verb = seg[0]
    if verb in danger_verbs:
        blocked = True
        break
    if verb == 'sed' and any(t == '-i' or t.startswith('-i') for t in seg[1:]):
        blocked = True
        break
    if verb == 'rsync' and '--delete' in seg:
        blocked = True
        break
    if verb == 'find' and '-delete' in seg:
        blocked = True
        break
    if verb == 'git' and len(seg) > 1 and seg[1] == 'clean':
        blocked = True
        break
    if any(t in ('>', '>>') for t in seg):
        blocked = True
        break

print("blocked" if blocked else "")
PYEOF
)

if [[ "$blocked" == "blocked" ]]; then
  "$PY" -c "
import json
reason = 'CLAUDE.mdの禁止事項により、obsidian_vault/raw/配下のファイルはAIが編集・削除できません（不変の原文ソースのため人間のみが書き込みます）。内容を反映したい場合は、/ingestでwiki/へ要約するか、変更が必要な理由をユーザーに確認してください。'
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': reason}}, ensure_ascii=False))
"
fi

exit 0
