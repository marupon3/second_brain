---
title: 複数生成AIの同時利用比較メモ
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2024-03-20 生成AI 同時利用.md
---

# 複数生成AIの同時利用比較メモ

同一のお題（Flaskで連動するプルダウンリストを実装する）を、複数の生成AIに同時に投げて回答を比較した記録。Anakin AI（<https://app.anakin.ai/apps/22112>）で複数AIへの一括プロンプト送信を行ったと見られる。

## 比較対象モデル

ChatGPT-4、Claude 3 Opus、Google PaLM 2、Mistral Large、Perplexity

## 所感（原文メモから）

- いずれのモデルもFlask + jQuery（Ajax）でカテゴリ選択→アイテムリスト絞り込みという基本構成に収束した
- ChatGPT-4とClaude 3 Opusはテンプレート・ルーティングまで含めた完成度の高いコードを提示
- PaLM 2は説明が簡潔でコード量も少なめ
- Mistral Largeは色→商品のようにやや異なるサンプルデータで具体例を構成
- Perplexityはプロダクション利用時の追加考慮事項（DB処理、入力バリデーション、エラー処理）にも言及

複数の生成AIに同じお題を投げて出力を比較することで、モデルごとの説明の丁寧さやコードスタイルの違いを把握する用途のメモ。
