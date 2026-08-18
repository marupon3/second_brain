---
title: 開発環境・自動化Tips
updated: 2026-08-18
source:
  - obsidian_vault/raw/notes/Tips/2024-01-23 Sharepoint to local.md
  - obsidian_vault/raw/notes/Tips/2024-02-24 VBA, Excelで0埋め.md
  - obsidian_vault/raw/notes/Tips/2024-03-24 JavaScriptチートシート.md
  - obsidian_vault/raw/notes/Tips/2024-04-14 VSCode.md
  - obsidian_vault/raw/notes/Tips/2024-06-12 windows11の修復.md
  - obsidian_vault/raw/notes/Tips/2025-05-16 CSSアコーディオンタグ.md
  - obsidian_vault/raw/notes/生成AI/2026-07-17 _ユーザインターフェイス.md
  - obsidian_vault/raw/notes/Python/2024-03-07 HTMLなしでWebページ作成.md
  - obsidian_vault/raw/notes/Python/2025-03-23 「Dockerって何？」.md
  - obsidian_vault/raw/notes/2026-07-29-OSSレベルの設計.md
---

# 開発環境・自動化Tips

## VSCode環境構築

- インストール: <https://code.visualstudio.com/download>
- Pythonフォーマッター(black)・リンター(flake8)拡張機能導入: <https://itc-engineering-blog.netlify.app/blogs/vscode-extensions-black-flake8>
- 導入拡張機能: `black`、`flake8`、`mypy Type Checker`
- 設定: 「Editor: Format On Save」にチェック

## JavaScriptチートシート

<https://jsprimer.net/cheatsheet/>（言語機能・データ構造・演算子・コントロールフロー・モジュール・プロジェクト構造を網羅）

## SharePoint⇔ローカルファイル連携（Python / shareplum）

```python
from shareplum import Office365
from shareplum.site import SharePlumSite
import os

sharepoint_url = "<https://your_sharepoint_site_url>"
username = "your_username"
password = "your_password"
authcookie = Office365(sharepoint_url, username=username, password=password).GetCookies()
site = SharePlumSite(sharepoint_url, authcookie=authcookie)

# アップロード
local_file_path = "C:\\path\\to\\your\\local\\file.txt"
sharepoint_folder_path = "/Shared Documents/FolderName"
with open(local_file_path, "rb") as file:
    file_name = os.path.basename(local_file_path)
    site.upload_file(file.read(), file_name, sharepoint_folder_path)

# ダウンロード
sharepoint_file_path = "/Shared Documents/FolderName/FileName.txt"
local_save_path = "C:\\path\\to\\save\\file.txt"
file_contents = site.get_file(sharepoint_file_path)
with open(local_save_path, "wb") as file:
    file.write(file_contents)
```

## VBA/Excelでの0埋め

```vba
Function ZeroPadString(Text As String, Length As Integer) As String
    ZeroPadString = Right(String(Length, "0") & Text, Length)
End Function
' 呼び出し例
Sub ExampleUsageString()
    Dim paddedString As String
    paddedString = ZeroPadString("abc", 5)
    Debug.Print paddedString  ' 出力: 00abc
End Sub
```

Excelの表示形式で0埋めする場合: `paddedValue = Format(originalValue, "000000")`

## Windows 11の修復（Windows Update関連の不具合）

`C:\Windows\SoftwareDistribution`フォルダを削除（データ紛失防止のため、削除前に`SoftwareDistribution.old`等へリネームすることを推奨）。

## CSSだけで作るアコーディオンUI

HTMLの`<details>`・`<summary>`タグで作るアコーディオンUI。CSSだけで開閉アニメーションを実装可能。`<details>`タグならブラウザ内検索でもキーワードがヒットするためユーザビリティも確保できる。

## デジタル庁デザインシステム（UI設計の参考資料）

デジタル庁が公開している「デザインシステム デザインデータ」（Figma、v2.16.0）。49コンポーネントの仕様、カラー・余白の基準、アクセシビリティガイドラインまで125ファイルで体系化されている。出典を明記すれば民間サイトでも利用可能。Claude Code等でAIにUIを作らせる際の設計基準として活用できる。

## MkDocs（HTML/CSS不要のWebページ作成）

Markdown形式で記述するだけでWebページを作成できるPython製ツール。複数のデザインテンプレートがあり、`.yaml`ファイルでデザインを調整可能。Markdownで書いた内容はHTMLに自動変換され、すぐに公開できる。

```
pip install mkdocs
```

## Dockerの基礎を絵で理解する

初心者向けにDockerの概念を図解した記事。<https://zenn.dev/suzuki_hoge/books/2021-04-docker-picture-60fbe950136be9c7ad85>

## AIに実装させることを前提とした設計書の書き方

一般的な設計書（要件定義→基本設計→詳細設計）は「人が読むため」で終わるが、生成AIに実装させることも目的にするなら「生成AIがそのまま実装できるレベル」を目標にした方が価値が高い。そのため各章の最後に必ず以下4項目を追加する。

1. **設計方針**: なぜこの設計を採用したのかを説明（例:「Providerをプラグイン方式にすることで、新しいAIサービス追加時の修正箇所を最小限に抑える」）
2. **実装ルール**: 実装時に守るルールを明文化（例:「Providerは必ずProviderBaseを継承すること」「APIキーをソースコードへ記述してはならない」）
3. **AI実装ガイド**: 生成AIへコード生成を依頼する際の条件（例:「Python 3.11を使用」「PEP 8準拠」「型ヒント必須」「docstring必須」「単体テストを書ける構造」「グローバル変数禁止」「`from x import *`禁止」）
4. **レビュー観点**

さらに、アーキテクチャ設計の前に「第0章 開発ガイドライン」を置くと全体の一貫性が高まる。含める項目例:

- **コーディング規約**: PEP 8準拠・型ヒント必須・docstring必須・UTF-8・行長100文字目安・f-string使用・`logging`使用（`print()`禁止）
- **ディレクトリ規約**: `app/`にアプリケーションコード、`tests/`にテストコード、`docs/`に設計書
- **クラス設計規約**: 1クラス1責務・継承よりコンポジション優先・抽象基底クラス（ABC）使用・`@dataclass`活用
- **例外設計規約**: `except Exception:`の安易な使用禁止・独自例外クラス定義・利用者向けメッセージとログ出力の分離
- **ログ規約**: INFO/WARNING/ERROR/CRITICALを用途ごとに使い分け
- **Git運用規約**: `main`（リリース）/`develop`（開発）/`feature/*`（新機能）/`fix/*`（不具合修正）
- **AIコード生成規約**: AIへ実装を依頼する際の共通ルール

この構成なら設計書は単なる仕様書ではなく、人にも読みやすく生成AIがそのまま実装できる「実装仕様書」になり、設計・実装・テスト・レビューまで一貫した品質基準を維持できる。

## 内容未記入のためページ化しなかったもの

`2025-06-20 CSS.md`、`2025-06-28 HTMLチートシート.md`、`2025-09-05 Vimコマンド.md`（notes/Tips/）、`2024-03-02 カスタマイズしたdockerイメージを作る.md`（notes/Python/）
