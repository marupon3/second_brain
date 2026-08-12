---
title: Pythonテキスト処理サンプル集
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2024-02-10 形態素解析（名詞頻度データ）.md
  - obsidian_vault/raw/notes/Python/2024-02-10 英単語出現頻度.md
  - obsidian_vault/raw/notes/Python/2024-02-17 高水準のファイル操作.md
  - obsidian_vault/raw/notes/Python/2024-02-18 ChromeDriver自動更新.md
  - obsidian_vault/raw/notes/Python/2024-02-20 PyPDF.md
  - obsidian_vault/raw/notes/Python/2024-02-25 pdfからtextを抜き出す試行錯誤のメモ.md
  - obsidian_vault/raw/notes/Python/2024-02-25 文章を句点区切りする.md
  - obsidian_vault/raw/notes/Python/2024-03-08 json.md
  - obsidian_vault/raw/notes/Python/2024-03-29 PythonでPDF操作.md
  - obsidian_vault/raw/notes/Python/2025-05-07 OCR機能向上.md
  - obsidian_vault/raw/notes/Python/2025-05-07 _Pathlib.md
  - "obsidian_vault/raw/notes/Python/2025-05-07 _Pathlib (2).md"
  - obsidian_vault/raw/notes/Python/2025-06-04 EasyOCR.md
---

# Pythonテキスト処理サンプル集

「Pythonプログラミング逆引き大全」の改良版サンプル、および標準ライブラリ活用メモ。

## 形態素解析による名詞頻度表の作成（要 analyzer.py）

Tkinterでファイル選択ダイアログを出し、テキストファイルを形態素解析して名詞の頻度表を作成・保存する。

```python
import os
import re
import analyzer
import tkinter as tk
from tkinter import filedialog

def make_freq(file):
    with open(file, 'r', encoding='utf_8') as f:
        text = f.read()
    text = re.sub('\n', '', text)
    word_dic = {}
    analyze_list = analyzer.analyze(text)
    for wd, part in analyze_list:
        if analyzer.keyword_check(part):
            word_dic[wd] = word_dic.get(wd, 0) + 1
    return word_dic

def save_analysis_results(file_path, word_dic):
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_形態素解析.txt"
    with open(new_file_path, 'w', encoding='utf_8') as f:
        for word, count in sorted(word_dic.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{word}: {count}\n")

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='ファイルを選択してください',
        filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
    )
    if file_path:
        freq = make_freq(file_path)
        save_analysis_results(file_path, freq)
```

## 英単語の出現頻度表を作成

```python
import os
import tkinter as tk
from tkinter import filedialog

def get_frequency(file_path):
    freq = {}
    with open(file_path, encoding='UTF-8') as file_data:
        for line in file_data:
            for word in line.split():
                word = word.rstrip('.,:!?)"').lstrip('("')
                freq[word] = freq.get(word, 0) + 1
    return freq

def save_frequency_list(file_path, freq):
    base, ext = os.path.splitext(file_path)
    new_file_path = f"{base}_英単語リスト.txt"
    with open(new_file_path, 'w', encoding='UTF-8') as file:
        for word in sorted(freq, key=freq.get, reverse=True):
            file.write(f"{word}, {freq[word]}\n")

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='ファイルを選択してください',
        filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
    )
    if file_path:
        freq = get_frequency(file_path)
        save_frequency_list(file_path, freq)
```

## shutilモジュール（高水準のファイル操作）

ファイル・ファイル群のコピーや削除などの高水準操作を提供する標準ライブラリ。個別ファイル操作は`os`モジュールも参照。<https://docs.python.org/ja/3/library/shutil.html>

## ChromeDriverの自動更新（Selenium）

`webdriver_manager`を使うとChromeDriverのバージョン管理・自動ダウンロードが不要になる。

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

ドライバーのインストール先例: `C:\Users\marupon\.wdm\drivers\chromedriver\win64\121.0.6167.184\chromedriver-win32`

## PyPDF（PDF自動化）

PythonでPDFを自動処理するライブラリ。

## PDFからテキストを抽出する試行錯誤メモ

**Unstructured**（2段組みのカラムを正確に検出できないという作者コメントあり）:

```python
from unstructured.partition.pdf import partition_pdf
pdf_elements = partition_pdf("pdf/7_71_5.pdf")
for structure in pdf_elements:
    print(structure)
```

**PyMuPDF (fitz)**:

```python
import fitz
doc = fitz.open("pdf/7_71_5.pdf")
out = open("output.txt", "wb")
for page in doc:
    text = page.get_text().encode("utf8")
    out.write(text)
    out.write(bytes((12,)))  # ページ区切り（フォームフィード）
out.close()
```

参考記事: <https://note.com/kan_hatakeyama/n/n1773c588ecb4>

## 文章を句点区切りにする（spaCy）

```python
import spacy
nlp = spacy.load('ja_core_news_sm')
text = "ここに日本語の文章を入力します。それぞれの文章は句点で区切られています。"
doc = nlp(text)
sentences = [sent.text for sent in doc.sents if sent.text.strip()]
```

モデルのダウンロード: `python -m spacy download ja_core_news_sm`

**文章の前処理技術（一般論）**: クリーニング（HTMLタグ等ノイズ除去）、正規化（全角/半角・大文字/小文字の統一）、文区切り（sentence segmentation）、単語分割（tokenization）、ストップワード除去。

参考: <https://qiita.com/heimaru1231/items/b6ed09d4787e4e28175a>

## JSON設定ファイルを複数のPythonファイルから共有する

`config.json`に設定値をまとめ、`config.py`で読み込み、他のモジュールから`config`変数として利用するパターン。

```python
# config.py
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()
```

```python
# main.py
from config import config

api_key = config["api_key"]
db_host = config["database"]["host"]
```

設定を一箇所（`config.json`）にまとめることで、アプリケーション全体の設定変更が容易になる。

## PythonのPDF操作ライブラリ比較

| ライブラリ | 主な用途 |
| --- | --- |
| pypdf | PDF生成、ページ分割・結合、途中挿入・回転、パスワード付与、テキスト/画像抽出、メタデータ |
| pdfminer.six | テキスト抽出、フォント取得 |
| pdfrw | PDF読込・書込 |
| reportlab | PDFへのテキスト・画像・図形の出力 |
| wkhtmltopdf / pdfkit | Web（HTML）ページのPDF化 |
| tabula-py | PDFから表（テーブル）を抽出 |
| PyMuPDF (fitz) | テキスト抽出、画像抽出、メタデータ |

## OCR精度向上の参考記事

- [OCRに関する技術調査 その2（PaddleOCRベースの精度改善検討）](https://zenn.dev/starai/articles/8871df599e967e)
- [Python&PlotlyでOCR結果を画像上でインタラクティブに可視化する](https://zenn.dev/yag_ays/articles/1142050914d510)

## pathlib（ファイル・パス操作の標準ライブラリ）

`os`や`glob`でも同様の操作は可能だが、`pathlib`はパスをオブジェクトとして扱えるため可読性が高い。

- 公式ドキュメント: <https://docs.python.org/ja/3/library/pathlib.html>
- 解説記事: <https://qiita.com/studio_haneya/items/11c9e825bd8068af7e87>、<https://www.jonki.net/entry/2024/02/17/232522>

## EasyOCR（手軽なOCRライブラリ）

80以上の言語に対応し、手書き文字・複数言語の同時認識も可能。

```python
import easyocr

reader = easyocr.Reader(['ja'])
results = reader.readtext("sample.jpg")
print(results)
```

結果は`(座標, 認識文字列, 確信度)`のタプルのリストで返る。

## 関連

- [[Python自然言語処理ライブラリ一覧]]
- [[pgroonga|PGroonga（PostgreSQL全文検索）]]（MeCab辞書設定は同ページ参照）
