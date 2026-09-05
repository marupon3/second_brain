# memory/ の目次

Skills が実行のたびに読み書きする永続状態。**Vault の中身（`wiki/` 等）ではなく、
Vault を作る側のルールと、その学習履歴**を置く。Obsidian のノートとしては扱わない。

| ファイル | 中身 | 書き手 | Git |
|---|---|---|---|
| `conventions.md` | 検証済みの恒久ルール。全 Skill が実行前に読む | `/dream` の提案 + 人間 | 版管理する |
| `lessons.md` | まだ規約として言い切れていない学び | `/dream` の提案 + 人間 | 版管理する |
| `violations.jsonl` | `/lint` が検出した違反の生記録 | `scripts/lint_vault.py --record` | 除外（再生成可能） |
| `violations-consumed.jsonl` | 規約へ昇格し終えた違反の退避先 | `scripts/dream_memory.py --archive` | 除外（再生成可能） |
| `proposals/` | `/dream` の提案。適用前の下書き | `/dream` | 除外（適用後は不要） |

## 学習ループ

```
/ingest /daily /weekly     conventions.md を読んで生成する
      ↓
/lint                      違反を決定的に検出し violations.jsonl へ記録する
      ↓
/dream                     何回再発したかを数え、規約への昇格を提案する
      ↓
人間が承認                 conventions.md へ追記し、記録を消化済みへ退避する
      ↓
次回の /ingest が、その規約を守った状態から始まる
```

判定を LLM の自己申告に委ねないため、違反の検出（`/lint`）と再発回数の集計
（`/dream`）はいずれも決定的なスクリプトが担当する。LLM が担うのは「規約として
どう書くか」の文言起こしだけで、`conventions.md` への適用には人間の承認を要する。
