---
created: 2026-08-18
source:
  - https://x.com/fleyta88/status/2087807308495519831
tags:
---
# メモリエンジニアリング

**要約：AIエージェントの「記憶」を正しく設計するための実践ガイド**

@fleyta88による投稿で、「エージェントがタスクを終えた後、同じユーザーが戻ってきても何も覚えていない」という問題を指摘し、**記憶（Memory）の設計**について体系的に解説しています。

### 核心的な指摘
- これはプロンプトやモデルの問題ではなく「ストレージ（記憶の保存方法）」の問題。
- 会話履歴を全部保存するのは「記憶」ではなく「トランスクリプト（文字起こし）」に過ぎない。
- 本当の記憶とは「その会話が終わった後も、将来必要になる事実」のこと。
### 7つのステップ（要点）
1. **保存するものを厳選する** 「この情報は将来のターンで参照されるか？」と問う。価格や決定事項は記憶、雑談や途中の選択肢は基本的に不要。
2. **取り出せなければ意味がない** 保存した事実には「明確な主語」「安定した表現」「スコープ（誰の情報か）」の3つが必要。スコープを忘れると、他人の情報が混ざる事故が起きる。
3. **記憶の形は主に3種類で十分**
    - **Working memory**：今のタスク中だけ（コンテキストウィンドウ）
    - **Episodic memory**：何が起きたか（この会話でXを決めた）
    - **Semantic memory**：永続的な事実（ユーザーの役割、好み、技術スタック） ほとんどのシステムはWorkingだけで終わり、重要な後者2つを作っていない。
4. **Retrieval（取り出し）は「フィルタ」であるべき** 関連しそうなものを全部入れるのではなく、「この事実が今の回答を変えるか？」で厳選する。書き込みは寛大に、読み込みは厳しく。
5. **モデルに「判断」、システムに「保存決定」を任せる** モデルに「これ覚えとくべき？」と聞くのは危険。モデルは提案だけさせ、別のルールで「本当に保存するか」を決める（プライバシー、重複チェックなど）。
6. **削除が最も重要な操作** 追加しかできないシステムは信用できない。ユーザーが「忘れて」と言ったら本当に消し、派生した情報も一緒に消す仕組みが必要。
7. **古くなる問題を無視するな** 事実にはタイムスタンプを付け、定期的に「まだ正しいか？」を確認する。古い情報を自動で優先順位下げたり、期限切れにする仕組みが必要。
### いつ記憶システムが必要か
- 同じユーザーが戻ってくる場合
- 個人化の価値が高い場合
- 正しく忘れることが重要な場合
一回きりのタスクなら、普通のコンテキストウィンドウで十分。
### 結論
- **Prompt engineering** → メッセージを良くする
- **Context engineering** → 1回の呼び出しで何を見せるかを制御
- **Memory engineering** → 呼び出しが終わった後も何を覚えているかを制御

これが揃って初めて、エージェントは「毎回初対面」を卒業できる、という内容です。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   [図: Memory Engineering ヘッダー図（テキスト化）]                          │
│                                                                             │
│   ┌──────────────┐     FROM CONTEXT WINDOW TO SYSTEM MEMORY                 │
│   │   CHAT       │                                                          │
│   │ WHAT IS      │     ┌─────────────────────────────────────────────┐      │
│   │ SHARED       │     │                                             │      │
│   │ MEMORY?      │     │          Memory Engineering                 │      │
│   │              │     │                                             │      │
│   │ HOW DOES     │     │  How AI stops forgetting and starts         │      │
│   │ CONTEXT      │     │  remembering                                │      │
│   │ WINDOW WORK? │     │                                             │      │
│   └──────────────┘     │            [full 7-STEP GUIDE]              │      │
│                        └─────────────────────────────────────────────┘      │
│                                                                             │
│   左: 会話ウィンドウ（CHAT）＋「FADED AWAY」矢印で消える様子                 │
│   中央: 大きな「Memory Engineering」タイトル＋脳と歯車のイラスト           │
│   右: データベース・ノート・検索・INTERNAL/EXTERNAL の流れ図                │
│       （FACT → EMBEDDED FACTS → RETRIEVAL → PROMPT など）                  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Memory Engineering: from a context window to a system that remembers      │
│  (full 7-step guide)                                                        │
│                                                                             │
│  An agent finishes a task at 9am. At 2pm the same user comes back with a    │
│  related question.                                                          │
│                                                                             │
│  The agent has no idea they ever spoke.                                     │
│                                                                             │
│  It re-asks what it already asked. It re-derives what it already derived.   │
│  It burns the same tokens twice and calls it a fresh start, because as far  │
│  as the context window is concerned, it is one.                             │
│                                                                             │
│  Nothing crashed. Nothing errored. The system just forgot, because nobody   │
│  designed it not to.                                                        │
│                                                                             │
│  That is not a prompting problem and it is not a model problem. It is a     │
│  storage problem wearing a conversation's clothes.                          │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 1. Most of what you save is not memory                                │
│                                                                             │
│  The instinct is to log everything: every message, every tool call, every   │
│  draft. That is not memory, that is a transcript, and a transcript is not   │
│  queryable, it is only re-readable from the top.                            │
│                                                                             │
│  Memory is not "what was said." Memory is "what should still be true, and   │
│  be retrievable, after the context that produced it is gone."               │
│                                                                             │
│  A price the user mentioned once is memory. The small talk around it is     │
│  not. A decision that was made is memory. The three options that were       │
│  rejected on the way to it, usually, are not.                               │
│                                                                             │
│  Ask one question of everything you're about to store: will a future turn   │
│  need to look this up, or does it only make sense next to the conversation  │
│  that produced it.                                                          │
│                                                                             │
│  If it only makes sense in place, it isn't memory. It's just context that   │
│  already did its job.                                                       │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 2. A fact you cannot retrieve is a fact you don't have                │
│                                                                             │
│  Writing something down is the easy half. The system only benefits from a   │
│  stored fact if something, later, actually goes and gets it, and gets the   │
│  right one, not an adjacent one.                                            │
│                                                                             │
│  That means every stored fact needs three properties: a clear subject, a    │
│  stable phrasing, and a scope.                                              │
│                                                                             │
│  Skip the scope field and you get the failure mode nobody notices until     │
│  it's embarrassing: one person's private detail surfacing in someone        │
│  else's session because it was filed under a shared key.                    │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 3. Three shapes cover almost everything                               │
│                                                                             │
│  You don't need a taxonomy of memory types. Production systems mostly need  │
│  three.                                                                     │
│                                                                             │
│  • Working memory. What's alive in the current task. Gone when the task     │
│    ends. This is just the context window, and it's fine for it to disappear.│
│                                                                             │
│  • Episodic memory. What happened. This conversation covered X, the user    │
│    decided Y on this date. Useful for continuity, rarely useful for         │
│    reasoning across many instances at once.                                 │
│                                                                             │
│  • Semantic memory. What's true, independent of when it was learned. The    │
│    user's role, their stack, their standing preferences. This is the        │
│    expensive one to get right, and the one worth the most.                  │
│                                                                             │
│  Most systems only build working memory and call it done. The gap between   │
│  "remembers the last message" and "remembers the user" is entirely          │
│  episodic and semantic memory, and almost nobody builds past the first.     │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 4. Retrieval is a decision, not a formality                           │
│                                                                             │
│  The default move is: stuff everything relevant-looking into the prompt     │
│  and let the model sort it out. That works until "everything relevant-      │
│  looking" is thousands of tokens of half-relevant history, and the model    │
│  starts weighting recency over relevance because recency is what's easiest  │
│  to attend to.                                                              │
│                                                                             │
│  Retrieval should be a filter, not a dump. Before something enters the      │
│  prompt, it should answer: does this change what I'm about to say. If a     │
│  stored fact wouldn't alter the response, it doesn't earn a place in it.    │
│  Decoration isn't retrieval, it's noise with good intentions.                │
│                                                                             │
│  Writing can be generous. Reading has to be strict, because every fact that │
│  gets in costs attention on every fact that matters more.                   │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 5. Let the model judge relevance, let the system decide storage       │
│                                                                             │
│  The tempting shortcut is to let the model decide, in the moment, whether   │
│  something is worth remembering. That's a judgment call buried inside a     │
│  generation task, made under time pressure, with no second opinion.         │
│                                                                             │
│  Split it, the same way you'd split classification from action anywhere     │
│  else.                                                                      │
│                                                                             │
│  The model proposes: "this looks durable, this looks worth keeping." A      │
│  separate, boring rule decides whether it's actually written: does it pass  │
│  the privacy filter, does a file already cover this subject, is it a fact   │
│  or an opinion the model formed.                                            │
│                                                                             │
│  This is also what keeps memory honest. A model under pressure to seem      │
│  attentive will over-remember and start inventing continuity that didn't    │
│  happen. A gate outside the generation step is what stops that.             │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 6. The most valuable operation deletes                                │
│                                                                             │
│  Every memory system that survives contact with real users eventually needs │
│  to forget something, and most systems have no path for it beyond "wait for │
│  the file to rot."                                                          │
│                                                                             │
│  Deletion has to be a first-class operation, not an afterthought bolted on  │
│  when someone complains. The user asks for a fact to be gone, and it's      │
│  actually gone, not softened into "used to be true." Anything derived from  │
│  a deleted fact gets removed too, not left standing on a foundation that no │
│  longer exists.                                                             │
│                                                                             │
│  A system that can only add is a system that eventually can't be trusted    │
│  with anything sensitive, because there's no way to take it back.           │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Step 7. Staleness is the part nobody diagrams                              │
│                                                                             │
│  A fact that was true in March is not automatically true in August. Roles   │
│  change, preferences change, projects end. Memory that never expires isn't  │
│  memory, it's sediment.                                                     │
│                                                                             │
│  The systems that hold up long-term timestamp what they store, prefer the   │
│  newest version of a fact over the oldest without deleting the trail        │
│  entirely, and periodically ask whether something still matches reality     │
│  instead of assuming permanence.                                            │
│                                                                             │
│  At any point, a memory system should be able to answer: how old is this    │
│  fact, and what would tell me it's gone stale. If it can't, it's a database │
│  with good intentions.                                                      │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  When memory is the wrong tool                                              │
│                                                                             │
│  Keep a plain context window when the task is one-shot, when nothing about  │
│  this user needs to carry forward, when the cost of re-asking is lower than │
│  the cost of a wrong recollection, and when nobody's coming back tomorrow.  │
│                                                                             │
│  Reach for a memory system when the same user returns, when facts genuinely │
│  outlive the conversation that produced them, when personalization is worth │
│  more than the tokens it costs, or when forgetting something correctly      │
│  matters as much as remembering it did.                                     │
│                                                                             │
│  Start with nothing stored. Add a file the first time forgetting actually   │
│  costs you something, not before.                                           │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  The layers, in order                                                       │
│                                                                             │
│  Prompt engineering improves the message.                                   │
│  Context engineering controls what the model sees in a single call.         │
│  Memory engineering controls what it still knows after the call is over.    │
│                                                                             │
│  Everything downstream of that is just an agent that finally stops meeting  │
│  you for the first time.                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
