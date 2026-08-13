---
title: Python基礎文法・命名規則メモ
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2024-02-19 プログラムのある絶対パス.md
  - obsidian_vault/raw/notes/Python/2024-02-28 エスケープシーケンス.md
  - obsidian_vault/raw/notes/Python/2024-02-28 コードの英語命名規則.md
  - obsidian_vault/raw/notes/Python/2024-04-18 インポートの記載順序.md
  - obsidian_vault/raw/notes/Python/2024-04-29 フォルダ構造を書くときの記号.md
---

# Python基礎文法・命名規則メモ

## プログラム自身の絶対パスを取得する

```python
import os
folder_path = os.path.dirname(__file__)
excel_file_path = folder_path + os.sep + "sample.xlsx"
```

フォルダ・ファイルパスの連結には`os.sep`を使う。

## エスケープシーケンス

| エスケープ文字 | 内容 |
| --- | --- |
| `\0` | NULL文字 |
| `\b` | バックスペース |
| `\n` | 改行（Line Feed） |
| `\f` | 復帰（Carriage Return） |
| `\t` | タブ |
| `\'` | シングルクォート |
| `\"` | ダブルクォート |
| `\\` | バックスラッシュ（円記号） |

## コードの英語命名規則

| 記法 | 説明 | 例 | Pythonでの使用箇所 |
| --- | --- | --- | --- |
| キャメル記法 | Pythonでは基本使わない | `userName` | - |
| パスカル記法 | Pascal言語由来 | `UserName` | クラス名 |
| スネークケース | - | `user_name` | モジュール名・メソッド名・関数名・変数名 |

詳細な命名フローチャート（変数のboolean/日時、関数の取得・変更・追加・作成・削除・検査・許可・禁止、クラスの命名パターン等）は下記記事に体系化されている。

参考: <https://qiita.com/hironori_narita/items/4b06db0953053d41c4a0>

その他の指針: 不可算名詞をなるべく使わない、二重否定を避ける、クラス名は単数形にする、必要に応じてデータ型を含める、否定形の形容詞を使う、動詞を複数使わない。

## importの記載順序（isort）

```
pip install isort
isort sample.py
```

標準ライブラリ→サードパーティ→自作モジュールの順に整列され、同一パッケージからの複数importは1行にまとめられる。

```python
import os
import sys
from third_party import (lib1, lib2, lib3, lib4, lib5)
from my_lib import Object, Object2, Object3
```

## フォルダ構造図を書くときの罫線記号

| 位置 | 文字 |
| --- | --- |
| たて | `│` `┃` |
| たてひだり | `┨` `┥` `┤` `┫` |
| たてみぎ | `┣` `┠` `┝` `├` |
| ひだりうえ | `┌` `┏` |
| ひだりした | `└` `┗` |
| ふとわく | `┗┻━┛` `┏┳━┓` |
| ほそわく | `└┴─┘` `┌┬─┐` |
| まんなか | `┼` `╋` `┿` `╂` |
| みぎうえ | `┐` `┓` |
