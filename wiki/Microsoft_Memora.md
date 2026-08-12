---
title: Microsoft Memora（AIエージェント向け長期記憶アーキテクチャ）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2026-07-01 _Microsoft.md
---

# Microsoft Memora（AIエージェント向け長期記憶アーキテクチャ）

Microsoft Researchが2026年6月29日（米国時間）に発表した、AIエージェントの「物忘れ」を防ぐための長期記憶アーキテクチャ「Harmonic Memory」。論文はICML 2026に採択、コードも公開済み（研究段階）。

## 課題認識

既存のAIエージェントの記憶手法にはそれぞれ弱点がある。

| 手法 | 特徴 | 課題 |
| --- | --- | --- |
| 会話履歴そのまま（完全なコンテキスト） | すべての情報を保持 | トークンが爆発的に増大し、コストが高い |
| RAG（全コンテキスト保存） | 必要な部分だけ検索 | 要約では細かい条件やニュアンスが消える |
| Mem0（重要事実のみ） | シンプルで軽量、重要な事実だけ保存 | 情報が断片化し、文脈・背景情報が消えやすい |
| GraphRAG（関係性をグラフで保持） | 複雑な関連を表現 | 記憶が細分化しやすく、ドメイン横断への汎化が難しい |

## Memoraのアーキテクチャ：Memory Entryを構成する3要素

「Memory Content（何を覚えるか）」と「Memory Structure（どう構造化してアクセスするか）」を分離した設計。

1. **Primary Abstraction（主抽象）**: 記憶を一意に表す6〜8語程度の安定したラベル（例: "Updated Project Orion timeline agreed by Dave and Sarah"）。Memory Valueが更新されても極力維持される
2. **Memory Value（記憶の中身）**: 関連するすべての詳細を統合・更新し続ける実データ。新しい出来事が起きるたびに追記・更新され、過去の文脈も保持
3. **Cue Anchors（手掛かりの集合）**: 人物・物事・イベント・トピックなど多様な切り口（Semantic Anchor）から同じ記憶へアクセス可能にする「入口」

## Policy-guided Retriever（探索アルゴリズム）

複数のCue（手掛かり）から同じ記憶にアクセスできる点は人間の記憶の想起プロセスに近い設計。Memoraは必要な情報が揃うまで探索方針を動的に調整しながらMemory Graph上を移動し、情報が十分になった時点で回答を生成する。

## ベンチマーク結果

LoCoMo（長期対話ベンチマーク、会話約600ターン）等でフルコンテキスト・RAG・Mem0と比較し、既存手法を上回る性能を達成（LLM-as-a-Judge評価）。コンテキスト効率（トークン使用量）はフルコンテキスト対比で大幅に削減。

## 現状まとめ

研究段階であり、Microsoft 365 Copilot等の製品への搭載については言及なし。

- 論文: arXiv:2602.03315（ICML 2026）
- コード: <https://github.com/microsoft/Memora>
- ブログ: <https://www.microsoft.com/en-us/research/blog/memora/>
