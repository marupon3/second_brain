---
title: PediaDose（個人開発Androidアプリ）
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/Android/2026-02-22 _Android_github使い方.md
  - obsidian_vault/raw/notes/Android/2026-02-24 _PMDAからデータ取得.md
  - obsidian_vault/raw/notes/Android/2026-02-24 _パッケージ構成.md
  - obsidian_vault/raw/notes/小児用量アプリ/2026-06-13 _PC→Andoroid.md
  - obsidian_vault/raw/notes/小児用量アプリ/2026-06-13 _PMDAから小児情報を取得.md
  - obsidian_vault/raw/notes/小児用量アプリ/2026-06-14 _新規薬剤追加手順.md
  - obsidian_vault/raw/notes/小児用量アプリ/2026-06-16 _データを上書きする手順.md
  - obsidian_vault/raw/notes/小児用量アプリ/2026-06-16 _手動で成人用量を入力.md
---

# PediaDose（個人開発Androidアプリ）

## 概要

PediaDoseは、小児用量計算を目的とした個人開発のAndroidアプリ。PMDA（医薬品医療機器総合機構）の添付文書データを取得し、薬剤情報・用量ルールを管理する。薬学的な内容は[[薬剤メモ]]も参照。

## アーキテクチャ

- MVVM + Repositoryパターン
- Single Activity / Jetpack Compose Navigation
- Room（ローカルDB）
- XmlPullParserによるPMDA RSS解析
- 手動DI（Applicationクラス、個人アプリのためHiltは不採用）

パッケージ構成（`com.marupon3.pediadose`）:

- `data/db/`: Room（`AppDatabase`、`entity/`、`dao/`）
- `data/network/`: `PmdaRssParser`（XmlPullParser実装）
- `data/repository/`: `DrugRepository`、`PmdaRepository`
- `domain/model/`, `domain/usecase/`: `CalculateDoseUseCase`、`CheckFreshnessUseCase`
- `ui/`: `navigation/`、`screen/`（home, dashboard, master, remaining, settings）、`component/`

## PMDA添付文書取得フロー

ボタン押下 → URL指定あり/なしで`fetchFromUrl()`または薬剤名検索`fetch()`を実行し、以下のステップで処理する。

1. PMDA接続（`fetchHtmlTyped()`）
2. HTTP応答確認
3. 詳細URL解決（`extractDetailUrl()`、検索の場合のみ）
4. HTML解析・抽出（`parsePackageInsert()`）
5. DB更新・転記（`repo.updateDrug()`）

### エラーコード一覧

| コード | 表示メッセージ | 原因 |
| --- | --- | --- |
| E101 | PMDAサイトに接続できません | DNS/TCP/SSL例外 |
| E102 | 添付文書データを取得できません（HTTP xxx） | 4xx/5xx応答 |
| E201 | 添付文書が見つかりませんでした | 検索結果に該当なし |
| E301 | 添付文書の情報を抽出できませんでした | HTMLは取得できたが全フィールドnull |
| E302 | 用量テキストが取得できませんでした | 改訂日・版数は取得済み、用量のみnull |
| E401 | 画面への転記に失敗しました | DB更新中に例外 |

## Windows⇔リモートのGit運用手順

ローカル（Windows）とリモートブランチ（例: `claude/update-android-build-config-Jc4EH`）間でpull/pushする際の手順。

1. `git status`で変更確認、あれば`git stash push -m "..."`で退避
2. `git fetch origin <branch>` → `git checkout <branch>` → `git pull origin <branch>`
3. 退避していた場合`git stash pop`（コンフリクト時は解決後`git add .` → `git stash drop`）
4. 変更をコミットし`git push -u origin <branch>`

## server/ ツール群（データ運用）

`server/tools/`配下のPythonスクリプトでPMDAデータの取得・整備を行う。

- **PMDAデータ取得**: `python tools/prefetch_pmda.py --max-candidates 0 <薬剤名>`で全件取得、薬剤名指定で個別更新、`--force`で改訂日同一でも強制更新
- **候補数確認**: `python tools/count_candidates.py --min N [--max M]`で候補件数の多い薬剤を確認
- **小児適応なし薬剤の洗い出し**: `python tools/cleanup_non_pediatric.py`（ドライラン、「小児/幼児/乳児/新生児/乳幼児/学童」の記載有無で判定）
- **新規薬剤追加**: PMDA検索結果を`results.txt`に保存 → `python tools/extract_generics_from_text.py results.txt --apply`で`prefetch_drugs.txt`に追記（`--strip-salts`で塩の正規化可）→ `prefetch_pmda.py`で一括取得 → APK再ビルド
- **APK転送**: `app/build/outputs/apk/debug/app-debug.apk`をGoogleドライブ経由でPC→Android転送

### データ上書きの実行順序（重要）

手動値を必ず最後に再適用するため、以下の順序を守る。

1. `python tools/prefetch_pmda.py` — PMDA再取得
2. `python tools/revalidate_doses.py` — 既存データの誤ルール除去
3. `python tools/backfill_adult_dose.py` — 成人量の自動補完
4. `python tools/apply_adult_overrides.py` — 手動の成人量を再適用（必ず最後）
5. APK再ビルド

### 手動での成人用量入力（漸増薬など自動読み取り不可の薬剤）

1. `git pull` → `cd server`
2. `copy data\adult_dose_overrides.example.json data\adult_dose_overrides.json`
3. `notepad data\adult_dose_overrides.json`を開き、`generic_name`ごとに`adult_max_per_dose`/`adult_max_per_day`（mg、数値は引用符なし）を記入。g単位はmgに換算（×1000）。両方nullなら安全のため無視される
4. `python tools/apply_adult_overrides.py`で反映（`generic_name`指定で同成分の全メーカー品に一括反映）
5. APK再ビルド

手動入力した値には「手動」の印がつき、以降の自動取得（backfill）で上書きされない。残件確認は`python tools/list_missing_adult.py`。

## 関連ページ

- [[薬剤メモ]]
