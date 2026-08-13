---
title: Mac Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Mac/2025-11-03 Youtubuの音声を保存.md
---

# Mac Tips

## yt-dlpでYouTube動画・音声を保存

```
brew install yt-dlp ffmpeg
```

mp4形式で保存:

```
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" -o "~/Movies/%(title)s.%(ext)s" <動画URL>
```

画質を720pに固定:

```
yt-dlp -f "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4" <動画URL>
```

音声のみ（m4a）保存:

```
yt-dlp -f bestaudio --audio-format m4a -o "~/Music/%(title)s.%(ext)s" <動画URL>
```

更新: `brew upgrade yt-dlp`。実行中の中断は`Ctrl + C`。

## 関連ページ

- [[windows-tips|Windows Tips]]
