#!/usr/bin/env bash
# 破壊的なGitコマンド（force push・reset --hard・clean -f・checkout/restore .・branch -D）を
# 対象パスに関わらずリポジトリ全体でブロックする。README.md「変更の切り戻し」の方針
# （git reset --hardを使わずgit revertで戻す）を機構的に裏付ける。
# block-raw-bash.shはobsidian_vault/raw/を対象にした場合のみブロックする設計だが、
# 本フックはGitの操作そのものが対象で、パスを問わない。
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
import shlex
import sys

try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit(0)

ti = data.get('tool_input') or {}
command = ti.get('command') or ''
if not command:
    sys.exit(0)

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

reason = None
for seg in segments:
    if len(seg) < 2 or seg[0] != 'git':
        continue
    sub = seg[1]
    args = seg[2:]

    if sub == 'push' and ('--force' in args or '-f' in args):
        reason = 'git push --force（強制push）はリモートの履歴を書き換えるため'
        break
    if sub == 'reset' and '--hard' in args:
        reason = 'git reset --hardは未コミットの変更を破棄するため'
        break
    if sub == 'clean' and (
        '--force' in args
        or any(t.startswith('-') and not t.startswith('--') and 'f' in t for t in args)
    ):
        reason = 'git clean -f系はコミットされていないファイルを削除するため'
        break
    if sub in ('checkout', 'restore') and '.' in args:
        reason = f'git {sub} .はワーキングツリーの未コミット変更を丸ごと破棄するため'
        break
    if sub == 'branch' and ('-D' in args or ('--delete' in args and '--force' in args)):
        reason = 'git branch -Dは未マージの変更を含むブランチを強制削除するため'
        break

if reason is None:
    sys.exit(0)

message = (
    'CLAUDE.mdの禁止事項（破壊的操作は実行前にユーザーへ確認）により、このGitコマンドは実行できません'
    f'（{reason}）。ユーザーに実行意図を確認するか、より安全な代替手段（git revert等）を検討してください。'
)
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': message}}, ensure_ascii=False))
"

exit 0
