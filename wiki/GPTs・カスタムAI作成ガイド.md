---
title: GPTs・カスタムAI作成ガイド
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2024-02-04 Hugging Face.md
  - obsidian_vault/raw/notes/生成AI/2024-02-07 7　GPTs 作成のコツ.md
  - obsidian_vault/raw/notes/生成AI/2024-02-07 Hugging faceのChatbot機能.md
  - obsidian_vault/raw/notes/生成AI/2024-02-09 GPTs作成ガイド.md
---

# GPTs・カスタムAI作成ガイド

## GPTs作成のコツ（時短ポイント）

1. 「Create」（誘導形式、英語で返ってくることが多い）は無視し、「Configure」にのみ日本語で望むAIの特徴を書き込めば十分
2. 「あなたは〜〜です」とAIの存在を明確に定義する（定義が曖昧だと出力が不安定になる）
3. 完成後は必ず「Preview」で動作確認し、違和感があれば「Instructions」を見直す

## プロンプト設計時に検討すべき22項目（GPTs作成ガイド）

トーン、フォーマット、役割、目的、コンテキスト、範囲、キーワード、制約、例、期限、対象者、言語、引用、視点、反論、用語、例え話、統計、視覚要素、行動呼び掛け、敏感なトピックの扱い等をプロンプト設計時にチェックリストとして検討する。

## Hugging Chat Assistants（OpenAI GPTsの無料オープンソース対抗）

Hugging FaceがOpenAIのGPTビルダーに対抗する無料サービス「Hugging Chat Assistants」を発表（2024年2月）。特徴:

- 多様なオープンソースLLMから選んで自分専用AIアシスタントを2クリックで作成可能
- 基本規制が少なく自由度が高い
- 他の人が作成したインストラクションがデフォルトで閲覧可能
- ブラウジング機能もGPTと同様に使用可能

## 関連

- [[生成AIプロンプト集]]
- [[生成AIツール・リンク集]]
