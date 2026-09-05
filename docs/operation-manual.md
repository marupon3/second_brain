# 運用手順書

対象: `second_brain`（第二の脳／Second Brainプロジェクト）

前提: 本プロジェクトはサーバーを持たないローカル完結型アプリケーション（`docs/basic-design.md` 1.1アーキテクチャ方針）である。そのため、一般的なWebサービスの運用手順書が扱う「デプロイ」「監視」「アラート」の多くは本プロジェクトにはそのままの形で存在しない。該当しない項目は、実態に即した代替手順に読み替えるか、「要確認」と明示している。

---

## 1. セットアップ手順・切り戻し手順

### 1-1. 新規セットアップ（デプロイに相当）

1. ベースキットをFork・ローカルにclone
2. 依存ツールを確認する

   ```
   python scripts/check_env.py
   ```

3. Vaultディレクトリ構造を生成する

   ```
   python scripts/setup.py
   ```

4. `CLAUDE.md`を確認・カスタマイズする
5. ObsidianでこのVaultフォルダを開く
6. Claude Codeをこのディレクトリで起動する

### 1-2. 切り戻し手順

変更を元に戻す必要が生じた場合、`git reset --hard`のような破壊的コマンドは使わず、以下の手順で行う。

1. `git log`で問題発生前のコミットを特定する
2. `git revert <コミットID>`で当該変更を打ち消す新しいコミットを作成する（履歴を破壊しない）
3. Obsidian側で開いているファイルがある場合は再読み込みする

---

## 2. 監視項目

本プロジェクトはローカル完結のため、外部監視基盤（メトリクス収集・アラート通知）は前提としていない（`docs/basic-design.md` 6.2「外部連携は現状最小限」）。代わりに、以下を利用者自身によるセルフチェックの目安とする。

| 項目 | しきい値の目安 | 出典 |
|---|---|---|
| ingest処理（記事・メモ1件） | 30〜90秒以内 | `docs/requirements.md` 6節Q4 |
| クエリ応答（`/query`） | 10〜30秒以内 | 同上 |
| lint（数百ページ規模） | 1〜3分以内 | 同上 |
| Daily Note生成 | 10秒以内 | 同上 |

上記を大きく超える場合は、Vaultのページ数増加が原因である可能性が高い。`docs/basic-design.md` 3.4節（ADR-4）のとおり、現状はインデックス機構を持たずファイルシステムを直接走査する設計のため、ページ数が増えるほど遅くなる。改善策（軽量インデックス導入等）の要否は**要確認**（本手順書では判断しない）。

自動アラート機構（しきい値超過時の通知等）は現時点の設計に含まれていない。**要確認**。

---

## 3. ログ

- `scripts/check_env.py` `scripts/setup.py` は標準出力・標準エラー出力にのみ結果を出力し、永続的なログファイルは生成しない（`output/architecture-plan.md` 5節の方針）。
- 保存先・形式・保存期間: 該当なし（永続ログを持たない設計のため）。
- Skills（`/ingest` `/daily` `/weekly` `/lint` `/query` `/dream`）の実行履歴は、`wiki/log.md`に記録される（`docs/basic-design.md` 4.2ページ種別）。保存期間の制限は設計上定められていない。**要確認**（無制限に追記され続けてよいかは未確定）。
- `/lint`が検出した違反は、`scripts/lint_vault.py --record`により`memory/violations.jsonl`へ1件1行のJSONとして追記される。これは`/dream`が再発回数を数えるための機械可読な記録であり、人間向けのレポートは`wiki/log.md`側にある。規約へ昇格し終えた分は`--archive`で`memory/violations-consumed.jsonl`へ退避する（7節）。いずれも`.gitignore`対象で、`/lint`を再実行すれば再生成できる。

---

## 4. 障害パターン別の初動手順

### 4-1. `check_env.py`が失敗する（終了コード1）
1. 出力された`[NG]`行を確認し、不足しているツール（Git / uv / pip / Python 3.11.9）を特定する
2. 該当ツールをインストールまたはバージョンを合わせる
3. `python scripts/check_env.py`を再実行し、終了コード0になることを確認する

### 4-2. `setup.py`が「対象パスがディレクトリではありません」で終了する（終了コード1）
1. 指定した対象パスが存在するファイルと衝突していないか確認する
2. 正しいディレクトリパスを指定し直して再実行する

### 4-3. `obsidian_vault/raw/`がAIによって編集された疑いがある
1. `git diff -- obsidian_vault/raw/`で変更内容を確認する
2. 意図しない変更であれば`git checkout -- obsidian_vault/raw/<該当ファイル>`（コミット前）または`git revert`（コミット後）で復元する
3. `CLAUDE.md`「4. 禁止事項」（obsidian_vault/raw/編集禁止）が正しく記載されているか確認する

### 4-4. `/lint`がリンク切れ・矛盾・規約違反を検出した
1. `/lint`の実行結果（レポート）を確認する。違反コード（`BROKEN_LINK` `ORPHAN_PAGE` `INDEX_MISSING` `INDEX_DANGLING` `FRONTMATTER_MISSING_KEY` `FRONTMATTER_BAD_DATE` `SKILL_NAME_MISMATCH`）が付いているものは、`memory/conventions.md`の同じコードの項目に対応する
2. 自動修正は行われない設計（`docs/requirements.md` 6節Q3）のため、手動で修正するか、Claude Codeに個別に修正を指示する
3. 同じ違反が実行のたびに再発する場合は、個別修正ではなく7節の学習ループで規約へ昇格させることを検討する（生成側が同じ失敗を繰り返さないようにするため）

### 4-5. 応答・処理が「2. 監視項目」の目安を大きく超える
1. Vaultのページ数（`wiki/`配下のファイル数）を確認する
2. 目安を大きく超える規模であれば、インデックス機構導入の要否を検討する（`docs/basic-design.md` 3.4節ADR-4参照）。対応方針は**要確認**

---

## 5. バックアップとリストア

`docs/requirements.md` 3.3節・`docs/basic-design.md` 8節に基づく。

- **取得方法**: Gitコミット、またはVaultフォルダ全体のコピーのいずれか
- **取得頻度**: 要件・設計書に定量的な指定はない。**要確認**（目安として日次のGitコミットを推奨するが、これは提案であり決定事項ではない）
- **保存先**: ローカルのGitリポジトリ、または任意の外部ストレージへのフォルダコピー（クラウド同期サービスへの依存は要件上「対象外」〈`docs/requirements.md` 1.3〉のため、自動クラウドバックアップは前提としない）
- **リストア手順**:
  1. Gitの場合: `git clone`で複製するか、対象コミットへ`git checkout <コミットID>`する
  2. フォルダコピーの場合: バックアップしたフォルダ全体を復元先にコピーする

---

## 6. 定期作業一覧

| 作業 | 頻度 | 出典 |
|---|---|---|
| Gitへのコミット | 要確認（`docs/basic-design.md` 8節は「定期的な」とのみ記載、具体的頻度なし） | `docs/basic-design.md` 8節 |
| `/lint`によるVault整合性チェック | 要確認（設計書に頻度の指定なし）。`/ingest`等でページを生成した直後の実行を推奨する | `docs/basic-design.md` 3.2節 |
| `/dream`による規約の見直し | `/lint`を3回以上実行して違反記録が貯まった時点（7節参照） | 本手順書7節 |
| 証明書更新・サーバー系メンテナンス | 該当なし（サーバーを持たないローカル完結型のため） | - |

---

## 7. 学習ループの運用

`/lint`が検出した違反を`/dream`が規約へ昇格し、次回以降の生成がその規約を守った状態から始まる、という1本のループを持つ（`CLAUDE.md` 6節）。本節はその運用手順を扱う。

### 7-1. 基本サイクル

```
python scripts/lint_vault.py --record   # 生成後に実行し、違反を記録する
python scripts/dream_memory.py          # 何が何回再発しているかを確認する
/dream                                  # 規約への昇格を提案させる（適用はしない）
（提案を目視して納得したら）「適用して」と指示する
python scripts/dream_memory.py --archive  # /dream が適用後に自動実行する
```

**`/dream`の提案は毎回目視する。** 適用を機械的に承認し続けると、意味的に同じだが文言の異なる規約が`memory/conventions.md`に積み上がる。文字列の正規化比較では言い換えを検出できないため、これは仕組みでは防げない（GrowLoopの基本設計書5.3節と同じ限界）。

### 7-2. `--record`を付け忘れたとき

`--record`なしの`python scripts/lint_vault.py`は表示のみで、`memory/violations.jsonl`に何も残らない。`/dream`の集計対象にならないため、学習に反映されない。表示だけ確認したい場合を除き、`--record`を付ける。

### 7-3. しきい値の考え方

`scripts/dream_memory.py`は既定で「3回以上の実行で出現した違反」を昇格候補とする。1回きりの違反を規約にすると、たまたま起きた事象を恒久ルールとして抱え込むことになるため、既定値を下げるのは慎重に判断する。

一時的に緩めたい場合は`--threshold 2`のように指定する（この指定は集計の表示にのみ影響し、記録側は変わらない）。

### 7-4. `memory/`のGit管理

| ファイル | Git | 理由 |
|---|---|---|
| `conventions.md` `lessons.md` `index.md` | 版管理する | 学習の結果そのもの。`git diff`で「何をいつ学んだか」を追える |
| `violations.jsonl` `violations-consumed.jsonl` `proposals/` | 除外（`.gitignore`） | `/lint`を再実行すれば再生成できる中間データ |

規約が意図せず変わった場合は`git diff -- memory/`で差分を確認し、`git revert`で戻す（1-2節の切り戻し手順と同じ）。

### 7-5. 障害パターン

**`/dream`が「違反記録がありません」と言う**
`/lint`を`--record`付きで実行していないか、直前に`--archive`で退避している。`python scripts/lint_vault.py --record`を実行してから再試行する。

**規約を`conventions.md`に書いたのに守られない**
生成系Skill（`/ingest` `/daily` `/weekly`）が`memory/conventions.md`を読む手順になっているか、各`SKILL.md`の「メモリ」節を確認する。読んでいるのに守られない場合は、規約の文言が曖昧である可能性が高い。検証手段（違反コード）と1対1で対応する断定形の一文に書き直す。

**同じ提案が毎回出る**
適用後に`python scripts/dream_memory.py --archive`を実行していない。退避しないと同じ違反記録が数え続けられる。

**検出結果が実態と合わない**
`scripts/`配下の判定ロジック（`find_wiki_issues.py`等）を手で直さない。これらはGrowLoopの生成物であり、次回の再生成で上書きされる。仕様を変える場合はGrowLoop側の`tasks/*.toml`を直して再生成する（GrowLoopの`integrations/second_brain/README.md`参照）。

---

## 8. 特記事項

- 本手順書は`docs/basic-design.md`（v1.1）・`output/architecture-plan.md`に基づき作成した。設計書に記載のない運用前提（監視しきい値超過時の対応方針、ログ保存期間の上限、バックアップ頻度）は推測で確定せず「要確認」とした。
