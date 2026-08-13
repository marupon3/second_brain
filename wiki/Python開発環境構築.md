---
title: Python開発環境構築メモ
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Python/2024-02-03 PyCharmインストール.md
  - obsidian_vault/raw/notes/Python/2024-02-04 Jupyter install.md
  - obsidian_vault/raw/notes/Python/2024-02-14 VSCode.md
  - obsidian_vault/raw/notes/Python/2024-02-15 ローカルリポジトリ作成.md
  - obsidian_vault/raw/notes/Python/2024-01-28 git Sourcetree.md
  - obsidian_vault/raw/notes/Python/2024-02-17 自動整形ツール「black」.md
  - obsidian_vault/raw/notes/Python/2024-02-19 Packaging.md
  - obsidian_vault/raw/notes/Python/2024-02-25 C++ Build Toolsのインストール.md
  - obsidian_vault/raw/notes/Python/2024-02-22 pass word管理.md
  - obsidian_vault/raw/notes/Python/2024-03-04 使用中のポートを解放する.md
  - obsidian_vault/raw/notes/Python/2024-03-10 pyinstaller.md
  - obsidian_vault/raw/notes/Python/2024-05-01 venv 仮想環境.md
  - obsidian_vault/raw/notes/Python/2024-05-30 pipダウンロード.md
  - obsidian_vault/raw/notes/Python/2024-06-22 pip.md
  - obsidian_vault/raw/notes/Python/2025-04-16 Visual Studioインストール.md
  - obsidian_vault/raw/notes/Python/2025-04-19 python-ldap download.md
  - obsidian_vault/raw/notes/Python/2025-04-26 _バージョンを指定して仮想環境を作成.md
  - obsidian_vault/raw/notes/Python/2025-04-26 _モジュール移行.md
  - obsidian_vault/raw/notes/Python/2025-04-29 _python3.11のインストール.md
  - obsidian_vault/raw/notes/Python/2025-12-28 _文法チェッカー（自作）.md
  - obsidian_vault/raw/notes/Python/2026-01-30 _PEP8対応.md
---

# Python開発環境構築メモ

## PyCharm

過去バージョン一覧: <https://www.jetbrains.com/ja-jp/pycharm/download/other.html>。2021.3.3をJupyter Notebook利用のため導入し、後に2025.1へアップデート（2025/4/25）。

### PyCharm 2021.3でのPackaging Toolsインストール

PyCharm 2021.3がPython 3.12に未対応のため、設定画面のインタープリターからPackaging Toolsがインストールできない場合、仮想環境のターミナルで以下を実行する。

```
python -m pip install --upgrade pip setuptools wheel
python -m pip install packaging tools
```

## Jupyter Lab

```
pip install jupyterlab
jupyter lab
```

実行するとブラウザでJupyterが開く。

## VSCode

導入した拡張機能: Python、Pylance、Isort、Jupyter、indent-rainbow、vscode-icons。仮想環境（venv）は`C:\Users\marupon\.vscode`、ワークスペースは`C:\Users\marupon\VSCode`に作成。

## Git / Sourcetree

- Sourcetreeの使い方解説記事: <https://mteam.jp/column/10210/>
- VSCode用ローカルリポジトリ作成手順: gitディレクトリ（例: `C:\Users\marupon\VSCode\作業用`）を用意し、Sourcetreeで「New tab」→「+（Create）」→保存先パスと名前を指定して「作成」

## black（自動整形ツール）

コーディング規約（PEP8）に従ったプログラムを書くための静的解析・自動整形ツール。プログラムを実行せずに内容をチェックできる。

```
py -m pip install black
py -m black "対象ファイルのフルパス"
```

## C++ Build Toolsのインストール

`pip install`時に「error: Microsoft Visual C++ 14.0 is required」が出た場合に必要。<https://visualstudio.microsoft.com/ja/visual-cpp-build-tools/>からインストーラーを実行し「C++ build tools」を選択（将来のビルドに備え「Windows 10 SDK」等の追加コンポーネントも選択推奨）。参考: <https://tech.nkhn37.net/python-pip-install-error-microsoft-visual-c-14/>

## パスワード・認証情報の安全な管理

### 方法1: python-dotenv

`.py`ファイルと同じ階層に`.env`ファイルを作成。

```
DB_USER=user_name
DB_PASSWORD=pass_word
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
```

### 方法2: keyringモジュール

OSのセキュリティシステム（Windowsでは資格情報マネージャー）で機密情報を保護する。

```
pip install keyring
```

```python
import keyring
keyring.set_password("system", "username", "password")
password = keyring.get_password("system", "username")
```

参考: [パスワードをハードコーディングしないためのTips](https://scrapbox.io/PythonOsaka/%E3%83%91%E3%82%B9%E3%83%AF%E3%83%BC%E3%83%89%E3%82%92%E3%83%8F%E3%83%BC%E3%83%89%E3%82%B3%E3%83%BC%E3%83%87%E3%82%A3%E3%83%B3%E3%82%B0%E3%81%97%E3%81%AA%E3%81%84%E3%81%9F%E3%82%81%E3%81%AETips)、[python-dotenvで環境変数を設定する](https://qiita.com/harukikaneko/items/b004048f8d1eca44cba9)

## 使用中のポートを解放する（Flask開発時）

Windowsで特定ポート（例: 5000）を使用しているプロセスを特定して終了させる。

```
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

Flaskアプリの起動方法（環境変数`FLASK_APP`の設定方法いくつか）:

```
set FLASK_APP=main:app
flask run
```

または`python main.py`で直接起動、`flask --app <main.pyの一つ上のフォルダ名> run`でも可。開発モードは`set FLASK_ENV=development`。

## venv仮想環境の基本操作

```
cd [プロジェクト名のパス]
python -m venv venv
venv\scripts\activate
python -m pip install --upgrade pip
pip install flask
```

環境変数を設定してFlaskアプリを起動:

```
set FLASK_APP=main.py
set FLASK_ENV=development
flask run
```

仮想環境から離脱・削除:

```
deactivate
rmdir /s /q venv
```

`/s`は指定ディレクトリ以下をすべて削除、`/q`は確認メッセージを出さない（QUIETモード）。

## PyInstallerでexe化

```
pyinstaller --onefile --windowed --hidden-import=processing --hidden-import=outlook --add-data "master/master1.csv;master/" --add-data "master/master2.csv;master/" --add-data "templates/index.html;templates/" --add-data "templates/result.html;templates/" main.py
```

`--onefile`で単一exeにまとめ、`--windowed`でコンソール非表示、`--hidden-import`で自動検出されないモジュールを明示、`--add-data`で同梱データファイルを指定する。

## pipのオフラインインストール（インターネット非接続サーバー向け）

インターネットに接続できる環境で`.whl`ファイルをダウンロードしておく。

```
python -m pip download -d C:\module pip
pip download fastapi
pip download uvicorn
```

対象サーバーで仮想環境に入り、ダウンロード済みファイルからインストールする。

```
venv\scripts\activate
cd C:\module
python -m pip install --no-index --find-links=. pip
pip install --no-index --find-links=. <モジュール名>
```

## よく使うpipコマンド一覧

| コマンド | 内容 |
| --- | --- |
| `pip install <ライブラリ名>` | インストール |
| `pip uninstall <ライブラリ名>` | アンインストール |
| `python -m pip install --upgrade pip` | pip自体を最新版に更新 |
| `pip install -U <ライブラリ名>` | ライブラリをアップグレード |
| `pip install <ライブラリ名>==<バージョン>` | バージョンを指定してインストール |
| `pip list` | インストール済みライブラリ一覧 |
| `pip freeze` | インストール済みライブラリ一覧（`requirements.txt`形式） |
| `pip list --outdated` | 最新版でないライブラリのみ表示 |
| `pip check` | 依存関係の確認 |
| `pip show <ライブラリ名>` | ライブラリの詳細情報 |
| `pip download <ライブラリ名>` | インストールせずファイルのみダウンロード |
| `pip help` / `pip <コマンド> -h` | コマンド・オプションのヘルプ表示 |

## Visual Studio（C++開発ツール）のインストール

[無償版Community エディション](https://visualstudio.microsoft.com/ja/vs/community/)を公式サイトからダウンロード。VSCodeでのC++設定は<https://code.visualstudio.com/docs/cpp/config-msvc>を参照。

## python-ldapのWindows向けビルド済みwhlインストール

公式PyPIにWindows向けビルドがない場合、非公式ビルドを利用する。

```
pip install python_ldap-3.4.4-cp39-cp39-win_amd64.whl
```

配布元: <https://github.com/cgohlke/python-ldap-build/releases>

## バージョンを指定して仮想環境を作成

複数バージョンのPythonが入っている環境で、特定バージョンを明示して仮想環境を作る。

```
py -0p                        # インストール済みPythonバージョン一覧とパスを表示
py -3.9 -m venv .venv39        # Python Launcherでバージョン指定
C:\Python39\python.exe -m venv venv   # フルパス指定でも可

.venv39\Scripts\activate
python --version               # Python 3.9.x と表示されればOK
```

## requirements.txtによるモジュール移行

```
pip freeze > requirements.txt
```

`requirements.txt`の記法例:

```
Flask==2.2.3          # 完全一致
requests>=2.28.0      # 範囲指定
numpy<1.25.0
pandas                # バージョン未指定（最新をインストール）
Django>=3.2,<4.0      # 複数条件の組み合わせも可能
```

新しい環境への導入:

```
cd C:\path\to\your_project
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Python 3.11/3.12のインストール

<https://www.python.org/downloads/windows/>からインストーラーを取得。導入後は既存プロジェクトの仮想環境を新バージョンで再構成する。

```
C:\Users\marupon\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
```

## コード品質チェックの自動化（ruff/flake8/pylint/mypy）

複数の静的解析ツールを一括実行する自作スクリプト`code_checker.py`。

```python
import subprocess
import sys
import shutil

def run_check(tool_name, command):
    print(f"\n{'='*20} {tool_name} のチェック開始 {'='*20}")
    if not shutil.which(command[0]):
        print(f"警告: {tool_name} がインストールされていないためスキップします。")
        return
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode == 0:
            print(f"✅ {tool_name}: 問題は見つかりませんでした！")
        else:
            print(f"⚠️ {tool_name}: いくつかの指摘事項があります。")
    except Exception as e:
        print(f"実行中にエラーが発生しました: {e}")

def main():
    if len(sys.argv) < 2:
        print("使用法: python code_checker.py <チェックしたいファイル名.py>")
        return
    target_file = sys.argv[1]
    checks = [
        ("Ruff (高速チェック/整形)", ["ruff", "check", target_file]),
        ("Flake8 (PEP8準拠チェック)", ["flake8", target_file]),
        ("Pylint (コード品質スコアリング)", ["pylint", target_file]),
        ("mypy (静的型チェック)", ["mypy", target_file]),
    ]
    for tool_name, command in checks:
        run_check(tool_name, command)

if __name__ == "__main__":
    main()
```

使い方: `python code_checker.py target.py`

## PEP8準拠チェック（CI/PyCharm向け）

```
pip install flake8 flake8-bugbear isort black
flake8 fulltextsearch/
isort --check fulltextsearch/     # importの並び順チェック
black --check fulltextsearch/     # blackフォーマット準拠チェック
```

行の長さ（E501）以外を自動修正したい場合はruffが便利。

```
pip install ruff
ruff check --fix --ignore E501 .   # 自動修正
ruff check --ignore E501 .         # 確認のみ（修正なし）
```
