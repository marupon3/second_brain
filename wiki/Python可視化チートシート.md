---
title: Python可視化チートシート（グラフ選択フローチャート）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2024-09-07 グラフ可視化.md
---

# Python可視化チートシート（グラフ選択フローチャート）

データの性質に応じたグラフ選択の目安（matplotlib/seaborn）。

| データの性質・目的 | グラフ種類 | 関数例 |
| --- | --- | --- |
| 全体からの割合を示したい | 円グラフ | `plt.pie(data)` |
| 時系列を示したい | 折れ線グラフ | `plt.plot(data)` |
| 複数属性ごとに比較したい（分布） | 箱ひげ図 | `plt.boxplot(data)` |
| 指標の形式で複数属性を比較したい | レーダーチャート | `Radar.plot(data)` |
| カテゴリ値×カテゴリ値の関係を見たい | ヒートマップ | `sns.heatmap(data)` |
| 連続値同士の関係を見たい | 散布図 | `plt.scatter(data)` |
