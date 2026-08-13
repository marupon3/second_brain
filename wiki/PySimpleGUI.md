---
title: PySimpleGUI（Python GUI作成ライブラリ）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/図書館で借りた本/2025-03-05 GUI画面操作.md
---

# PySimpleGUI（Python GUI作成ライブラリ）

数あるGUIライブラリの中でも扱いやすいとされるPython製ライブラリ。

```
pip install pysimplegui
```

## 基本形の例

```python
import PySimpleGUI as sg

layout = [
    [sg.Text('お名前は？')],
    [sg.Input(key='name')],
    [sg.Button('決定', key='bt')]
]
window = sg.Window('こんにちは', layout)
event, values = window.read()
if event == 'bt':
    sg.popup(values['name'] + 'さんありがとうございます')
window.close()
```

テキスト表示・入力欄・ボタンでレイアウトを定義し、`window.read()`でイベントループを回す。ボタン押下イベントに応じてポップアップ表示などの処理を行う。

出典はOneNote画像のOCR変換テキストのため、レイアウト定義部分の記法は上記の通り簡略化して再構成した。実装時は公式ドキュメントで構文を確認すること。
