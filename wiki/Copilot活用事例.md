---
title: Microsoft Copilot / Copilot Studio 活用事例
updated: 2026-08-09
source:
  - obsidian_vault/raw/notes/生成AI/2026-07-01 _Copilot.md
  - obsidian_vault/raw/notes/生成AI/2026-07-25 _Copilot Studioできること.md
  - obsidian_vault/raw/notes/生成AI/https___github.com_yuichi-masuda_CopilotStudio-MeetingSchedulingAgent-Japanese.md
---

# Microsoft Copilot / Copilot Studio 活用事例

## Word × Copilotでの契約書編集

Word内でCopilotに「契約期間と支払い条件を一括払いに変更して」等と自然言語で指示すると、該当条項（協議事項・準拠法・変更履歴等）を含む契約書ドラフトを推論ステップ付きで一括編集してくれる。変更履歴（版・更新日・更新者・変更箇所・変更理由）も文書内で管理する運用例。

## Copilot Studioに任せられる業務8選

1. 社内ヘルプデスクの一次対応（使い方・営業時間・在庫等の定番質問に回答）
2. 顧客からの問い合わせ対応
3. 社内資料からの検索回答（PDF資料を読み解き根拠付きで回答）
4. 申請フォームの受付・登録（担当へ通知）
5. 経費・申請の一次チェック（確認・差し戻しでミスを防止）
6. 会議の日程調整（空き確認・候補出し・招待送信）
7. 定型レポートの定期作成・配信
8. 情報収集の見張りと通知（重要情報を見逃さず要点を通知）

## Copilot Studio会議調整エージェントのサンプル実装

Copilot Studio / M365 Copilotですぐ利用できる「会議調整エージェント」のOSSサンプル。LLM＋コードインタプリターの組み合わせで複雑な日程調整ケースにも対応。

<https://github.com/yuichi-masuda/CopilotStudio-MeetingSchedulingAgent-Japanese>
