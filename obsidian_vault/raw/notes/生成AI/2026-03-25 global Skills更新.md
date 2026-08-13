---
メモ: 2026-03-25
source: OneNote
作成時刻: 17:10
---

# _global Skills更新

今後の更新手順（これだけでOK）
powershell
cd ~\.claude\repos\anthropic-skills
git pull
シンボリックリンク経由で自動的に全スキルに反映されます。再起動不要です。
作業全体のまとめ
|  |  |  |
| --- | --- | --- |
| 手順 | 内容 | 状態 |
| 1 | ~\.claude\repos\ にリポジトリをクローン | 完了 |
| 2 | 開発者モードを有効化 | 完了 |
| 3 | シンボリックリンクを一括作成 | 完了 |
| 4 | Claude Code で動作確認 | 完了（前回済み） |
以上でGitHubスキルのリポジトリ管理による導入が完了しました。
PS
C:\Users\marupon> $src =
"$env:USERPROFILE\.claude\repos\anthropic-skills\skills"
PS
C:\Users\marupon> $dst = "$env:USERPROFILE\.claude\skills"
PS
C:\Users\marupon>
PS
C:\Users\marupon> Get-ChildItem $src -Directory | ForEach-Object {
>>     New-Item -ItemType SymbolicLink -Path
"$dst\$($_.Name)" -Target $_.FullName
>> }
Directory: C:\Users\marupon\.claude\skills
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
l----          2026/03/25    17:08                algorithmic-art ->
C:\Users\marupon\.claude\repos\anthropic-skills\sk
ills\algorithmic-art
l----          2026/03/25    17:08                brand-guidelines ->
C:\Users\marupon\.claude\repos\anthropic-skills\s
kills\brand-guidelines
l----          2026/03/25    17:08                canvas-design ->
C:\Users\marupon\.claude\repos\anthropic-skills\skil
ls\canvas-design
l----          2026/03/25    17:08                claude-api ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills\
claude-api
l----          2026/03/25    17:08                doc-coauthoring ->
C:\Users\marupon\.claude\repos\anthropic-skills\sk
ills\doc-coauthoring
l----          2026/03/25    17:08                docx ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills\docx
l----          2026/03/25    17:08                frontend-design ->
C:\Users\marupon\.claude\repos\anthropic-skills\sk
ills\frontend-design
l----          2026/03/25    17:08                internal-comms ->
C:\Users\marupon\.claude\repos\anthropic-skills\ski
lls\internal-comms
l----          2026/03/25    17:08                mcp-builder ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills
\mcp-builder
l----          2026/03/25    17:08                pdf ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills\pdf
l----          2026/03/25    17:08                pptx ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills\pptx
l----          2026/03/25    17:08                skill-creator ->
C:\Users\marupon\.claude\repos\anthropic-skills\skil
ls\skill-creator
l----          2026/03/25    17:08                slack-gif-creator ->
C:\Users\marupon\.claude\repos\anthropic-skills\
skills\slack-gif-creator
l----          2026/03/25    17:08                theme-factory ->
C:\Users\marupon\.claude\repos\anthropic-skills\skil
ls\theme-factory
l----          2026/03/25    17:08                web-artifacts-builder ->
C:\Users\marupon\.claude\repos\anthropic-ski
lls\skills\web-artifacts-builder
l----          2026/03/25    17:08                webapp-testing ->
C:\Users\marupon\.claude\repos\anthropic-skills\ski
lls\webapp-testing
l----          2026/03/25    17:08                xlsx ->
C:\Users\marupon\.claude\repos\anthropic-skills\skills\xlsx
