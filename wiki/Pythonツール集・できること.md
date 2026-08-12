---
title: Pythonでできること・ツール集
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2024-03-16 Pythonでできること.md
  - obsidian_vault/raw/notes/Python/2024-03-24 pythonツール集.md
  - obsidian_vault/raw/notes/Python/2024-03-31 顔認識.md
  - obsidian_vault/raw/notes/Python/2024-04-22 Streamlit データ可視化・分析.md
  - obsidian_vault/raw/notes/Python/2024-04-06 京大資料.md
  - obsidian_vault/raw/notes/Python/2024-03-18 Python早見表@東工大.md
---

# Pythonでできること・ツール集

## Pythonで業務効率化できる代表例

スクレイピング、Excel/Googleスプレッドシートの自動化、ファイル・フォルダの自動操作、デスクトップ操作、API利用、メール関連、データ分析・レポート自動化、ブラウザ操作、画像編集、PDF操作。参考: <https://trends.codecamp.jp/blogs/media/work-optimization-with-python>

## Flask製・複数ツール統合ポータルサイトの構成例

複数のPython処理ツール（文字数カウント、PDFテキスト抽出等）を1つのWebポータルにまとめる個人プロジェクトの構成。

```
Flask_Processing_Project/
├── app/
│   ├── templates/
│   │   ├── upload.html      # 処理用ファイルを選択
│   │   ├── menu.html        # 実行する処理を選択
│   │   ├── result.html      # 結果を表示
│   │   └── download.html    # ダウンロードボタンを表示
│   ├── __init__.py
│   ├── processing.py        # データ処理本体
│   └── routes.py            # アップロード/ダウンロードのルーティング
├── upload/                  # 処理前ファイルの保管
├── download/                # 処理後ファイルの保管
└── run.py                   # アプリケーション起動ファイル
```

ルーティングの骨格（`/`→アップロード画面、`/upload`→ファイル受け取り、`/process/<filename>`→処理選択・実行）を用意し、`action`パラメータで処理の種類（例: `character_count`）を分岐する設計。開発時のルール例: 実行ファイル`run.py`・初期設定`__init__.py`は変更せず追加のみ許可、既存の実装済み機能に影響を与えない形で新機能を追加する。

## 顔認識（DeepFace）

```
pip install deepface
```

```python
from deepface import DeepFace

objs = DeepFace.analyze(img_path="img.jpg", actions=['age', 'gender', 'race', 'emotion'])
result = DeepFace.verify(img1_path="img1.jpg", img2_path="img2.jpg")
```

年齢・性別・人種・感情の推定や、2枚の画像の同一人物照合ができる。

## Streamlit（データ可視化・分析アプリ）

Pythonだけでデータ可視化・分析アプリを高速に作成できるライブラリ。入門動画: <https://www.youtube.com/watch?v=zp-kAt1Ih5k>

## 学習資料リンク

- 京都大学のPython学習資料（PDF）: <https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/265459/1/Version2021_10_08_01.pdf>
- Python早見表（東京工業大学、chokkan氏）: 基本計算・変数・実行制御・関数・モジュールの基礎から、リスト・タプル・文字列・辞書・集合のデータ構造、ファイル入出力・クラス・例外・イテレータ等の発展、NumPy・Matplotlibまで体系的に整理。<https://chokkan.github.io/python/03control.html>
