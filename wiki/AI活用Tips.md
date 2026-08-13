---
title: AI活用Tips
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Tips/2023-07-13 AIアプリ開発.md
  - obsidian_vault/raw/notes/Tips/2024-01-22 プレゼン作成支援.md
  - obsidian_vault/raw/notes/Tips/2024-04-18 AI便利ツール.md
  - obsidian_vault/raw/notes/Tips/2024-05-11 コードを綺麗に.md
  - obsidian_vault/raw/notes/Tips/2024-06-24 コードを書かせるプロンプト.md
  - obsidian_vault/raw/notes/Tips/2024-06-27 短文、長文比較.md
  - obsidian_vault/raw/notes/Tips/2026-03-16 _生成AI画像を削除.md
  - obsidian_vault/raw/notes/Tips/240620 Unique3D.md
  - obsidian_vault/raw/notes/Tips/2025-11-21 _【入門】要件定義.md
  - obsidian_vault/raw/notes/Python/2025-03-28 AIエージェント.md
---

# AI活用Tips

## AIアプリ開発の参考資料

- [Zenn: AIアプリ開発関連書籍](https://zenn.dev/ml_bear/books/d1f060a3f166a5/viewer/f11592)
- OCRツール EzOCR（PDF領域OCR）: <https://ezocr.net/Areaocr_PDF>

## プレゼン作成支援

書籍『ヒト×AIでつくる未来のプレゼン　ChatGPTといっしょに、パワポスライドを「超時短」で仕上げてみた。』サンプルDL: <https://books.mdn.co.jp/books/3223303020/>

## AI便利ツール

| ツール | 用途 |
| --- | --- |
| [Gladia](https://www.gladia.io/) | 音声データの文字起こし・翻訳・分析 |
| [create](https://create-xyz-fyi.webflow.io/internal-tools) | ノーコードでWebサイト・アプリを開発できるAIツール |
| [Clipdrop](https://clipdrop.co/) | 画像生成・編集AIツール。Cleanup（不要箇所削除）、Image upscaler（解像度調整）、Relight（照明調整）、Remove/Replace background（背景除去・変更）、Reimagine XL（類似画像生成）、Sky replacer、Swap（人物入れ替え）、SDXL Turbo、Stable Diffusion XL、Stable Doodle、Text remover、Uncrop等の機能を搭載 |

## コードレビューをAIにさせる

Claude 3 Opus等にコードレビューさせる際のプロンプト例:

> Pretend you are a Senior Software Engineer, and review my code below to improve readability.

## コードを書かせる際の詳細プロンプトテンプレート

フルスタックエンジニアとしてロールを与え、「タスク分析→計画→美学とデザイン(任意)→コーディング→検証」の思考の連鎖に従わせるプロンプト。要点:

- タスクの要件を十分理解してから段階的に計画を立て、計画確定前にコードを書かない
- 各ステップの思考プロセスを説明してからクリーンで最適化されたコードを書く
- 修正依頼時は省略せず修正済みの完全なスクリプトを提供させる
- 複雑なロジック・エッジケース・エラー処理にコメントを付けさせる
- 「ここに他の関数が続く」等の省略フレーズを禁止し、完全なソリューションを要求する
- 検証ステップでバグを見つけたら全体を書き直させる

## AI学習用：短文回答と長文回答の比較分析

| | 利点 | 課題 |
| --- | --- | --- |
| 短文回答 | 簡潔性、処理効率、特定性、多様なトピックをカバー | 文脈の欠如、複雑な概念の説明が困難 |
| 長文回答（短文の10倍程度） | 豊富な文脈、複雑な概念の説明、自然な文章構造の学習 | ノイズ増加、処理効率低下、過学習リスク |

要約タスクには長文回答、質問応答には短文回答が向く。AI学習用途では一般に短文回答（高い情報密度・効率的処理・過学習リスク低減）が適するが、タスク性質に応じた組み合わせが効果的。

## Adobe Fireflyの生成AI画像を削除

生成履歴タブ（<https://firefly.adobe.com/your-stuff?tab=generationHistory>）から対象を選び「完全に削除」を選択する。

## Unique3D（1枚の画像から3Dメッシュ生成）

1枚の画像から高品質な3Dメッシュを高速生成できるAIツール。<https://gigazine.net/news/20240620-unique3d/>

## Browser Use（AIエージェントによるブラウザ自動操作）

```
pip install browser-use
playwright install
```

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI
import asyncio

llm = ChatOpenAI(model="gpt-4o-mini")
task = "今日の東京の天気を教えて"
agent = Agent(task=task + " 日本語に訳して", llm=llm)

async def main():
    await agent.run()

asyncio.run(main())
```

指示するだけでAIエージェントがWebを自動検索し、結果を要約して返す（例: Yahoo天気から情報取得）。

## 要件定義入門

参考記事: <https://zenn.dev/sutamac/articles/351cb3c7ea66ba>

## 内容未記入のためページ化しなかったもの

`生成AI後の新職業.md`、`perplexity AI.md`、`生成AI 分野別おすすめ.md`
