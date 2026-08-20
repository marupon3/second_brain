#!/usr/bin/env bash
# CLAUDE.md 4節: obsidian_vault/raw/配下のファイルはAIが編集・削除してはならない。
# Edit/Write/NotebookEditツールがraw/配下を対象にした場合はブロックする。
set -euo pipefail

input=$(cat)
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')

if [[ -z "$path" ]]; then
  exit 0
fi

if [[ "$path" == *"obsidian_vault/raw/"* ]]; then
  jq -n --arg reason "CLAUDE.mdの禁止事項により、obsidian_vault/raw/配下のファイルはAIが編集・削除できません（不変の原文ソースのため人間のみが書き込みます）。内容を反映したい場合は、/ingestでwiki/へ要約するか、変更が必要な理由をユーザーに確認してください。" \
    '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":$reason}}'
  exit 0
fi

exit 0
