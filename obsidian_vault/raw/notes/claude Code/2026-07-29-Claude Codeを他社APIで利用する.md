---
created: 2026-07-29
tags: Claude
---
# Claude Codeを他社APIで利用する

pythonで作成。
pycharmProjects\ai-provider-gateway
<使い方>
cd
C:\Users\marupon\PycharmProjects\ai-provider-gateway
git pull origin
main
.\scripts\run-claude.ps1   (デートウェイ経由 Groq, OpenRouter)
.\scripts/run-claude-direct.ps1（Claude経由）
<ゲートウェイを経由せず、直接
Anthropic の API と話す設定>
#
ゲートウェイ用の環境変数をこのセッションから消す
Remove-Item
Env:\ANTHROPIC_BASE_URL -ErrorAction SilentlyContinue
Remove-Item
Env:\ANTHROPIC_AUTH_TOKEN -ErrorAction SilentlyContinue
claude
最新情報
<コマンドに直接打つ>
provider           #
ゲートウェイ経由（無料プロバイダー）→.\scripts\run-claude.ps1不要
nonprovider     # 実 Claude（Anthropic API）
![](file6507.files/image001.png)
![](file6507.files/image002.png)
