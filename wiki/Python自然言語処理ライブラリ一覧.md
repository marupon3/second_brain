---
title: Python自然言語処理ライブラリ一覧
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2025-07-25 _自然言語処理.md
---

# Python自然言語処理ライブラリ一覧

用途別のNLP手法と代表的なPythonライブラリの対応表。

| 手法 | 概要 | 代表的ライブラリ |
| --- | --- | --- |
| 形態素解析 | テキストを単語や形態素に分割 | MeCab, Janome |
| 品詞タグ付け | 単語に品詞のタグ付け | NLTK, spaCy |
| 構文解析 | 文の構造を解析 | spaCy, NLTK |
| 文法チェック | 文法の誤りを検出 | LanguageTool |
| スペルチェック | スペルの誤りを検出 | pyspellchecker |
| キーワード抽出 | 重要なキーワードを抽出 | Rake-NLTK |
| テキスト分類 | テキストをカテゴリに分類 | scikit-learn |
| 感情分析 | テキストの感情を判定 | VADER, TextBlob |
| 固有表現抽出 | 人名・地名等の固有名詞を認識 | spaCy, NLTK |
| 共参照解析 | 指示語の参照先を特定 | spaCy, neuralcoref |
| テキスト要約 | 長い文章を短くまとめる | Gensim, Sumy |
| テキスト生成 | 自動で新しいテキストを作る | GPT系, T5 |
| テキストクラスタリング | 類似した文書をグループ化 | scikit-learn |
| トピックモデル | 文書のトピックを識別 | LDA, Gensim |
| パラフレーズ生成 | 意味が同じ文を生成 | Pegasus, T5 |
| テキスト類似度計算 | 文の類似度を計算 | scikit-learn, spaCy |
| 言語モデル | 単語・文章の予測モデルを作成 | GPT系, BERT |
| 機械翻訳 | テキストを他言語に翻訳 | Google Translate API |
| テキスト整形 | テキストの形式を整える | BeautifulSoup |
| 感情変換 | 感情の強弱を変える | VADER, TextBlob |
| テキスト校正 | 文書の誤りを修正 | LanguageTool |
| 感情強度分析 | テキストの感情の強度を評価 | VADER, TextBlob |
| 質問応答システム | 自然言語での質問に答えるシステム | BERT, GPT系 |
| テキストエンコーディング | テキストを数値ベクトルに変換 | Sentence-BERT |
| テキストランキング | 文書を重要度順に並べる | TF-IDF, BM25 |
| 可読性評価 | テキストの読みやすさを数値化 | Textstat |
| 談話解析 | 会話や文章の文脈を解析 | spaCy, NLTK |
| テキスト正規化 | テキストを正しい形式に変換 | NLTK |

## 関連

- [[Pythonテキスト処理サンプル]]（spaCyによる句点区切りサンプル等）
