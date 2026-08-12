---
title: openpyxlでExcel自動化
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2025-02-14 PythonでExcel自動化.md
---

# openpyxlでExcel自動化

openpyxlライブラリの主要メソッド・機能一覧。

| メソッド/機能 | 処理内容 |
| --- | --- |
| `load_workbook()` | Excelファイルを読み込む |
| `save()` | ワークブックを指定したファイル名で保存 |
| `create_sheet()` | 新しいシートを作成 |
| `remove()` | 指定したシートを削除 |
| `copy_worksheet()` | シートをコピー |
| `cell()` | 指定した行と列のセルを取得または作成 |
| `merge_cells()` | セルを結合 |
| `unmerge_cells()` | 結合されたセルを分割 |
| `iter_rows()` | 行に沿ってセルの値を反復処理 |
| `iter_cols()` | 列に沿ってセルの値を反復処理 |
| `add_chart()` | シートにチャートを追加 |
| `add_image()` | シートに画像を追加 |
| `BarChart()` / `LineChart()` / `PieChart()` / `ScatterChart()` / `BubbleChart()` / `RadarChart()` / `StockChart()` / `AreaChart()` | 各種グラフ（棒・折れ線・円・散布図・バブル・レーダー・株価・面）を作成 |
| `tabColor` | シートタブの色を設定 |
| `defaultRowHeight` / `defaultColWidth` | デフォルトの行の高さ・列の幅を設定 |
| `paperSize` | 印刷時の用紙サイズを設定 |
| `PatternFill()` | セルの背景色を設定 |
| `Border()` | セルの枠線の色を設定 |
| `GradientFill()` | セルにグラデーションの背景色を設定 |
| `Font()` | フォントを指定（グラフ要素の色はRGB値で指定可能） |
