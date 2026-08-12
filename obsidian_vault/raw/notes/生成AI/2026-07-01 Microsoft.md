---
メモ: 2026-07-01
source: OneNote
---

# _Microsoft

Memora
2026年7月1日
水曜日
5:51
![Microsoft 新 技 術 「 Memora 」 と は ?
Microsoft Research Blog
2026 年 6 月 29 日 ( 米 国 時 間 米 ) 発 表
AI エ ー ジ ェ ン ト の “ 物 忘 れ ” を 防 ぐ 長 期 記 憶 ア ー キ テ ク チ ャ
論 文 :ICML 2026 採 択
Microsoft Research が 開 発 し た 、 抽 象 と 詳 細 の 調 和 に よ る 次 世 代 メ モ リ シ ス テ ム (Harmonic Memory)
コ ー ド 公 開 済 み ( 研 究 段 階 )
※ 日 本 時 間 で は 6 月 30 日
1
な ぜ 新 し い 記 憶 ア ー キ テ ク チ ャ が 必 要 な の か
2
既 存 手 法 と の 比 較
現 在 の AI エ ー ジ ェ ン ト は 、
し か し 、 課 題 が あ る ...
手 法
特 徵
会 話 終 了 で 記 憶 が リ セ ッ ト さ れ る
会 話 履 歴
す べ て の 情 報 を 保 持
ト ー ク ン が 爆 発 的 に 増 大
ま た は 、 以 下 の 方 法 に 依 存 し て い る
×
ト ー ク ン コ ス ト の 増 大
そ の ま ま
( 完 全 な コ ン テ キ ス ト )
コ ス ト が 高 い
長 い 履 歴 を 毎 回 読 み 込 む
×
要 約 で は 細 か い 条 件 や
RAG
必 要 な 部 分 だ け 検 索
関 連 情 報 を 取 り 逃 が す
( 全 コ ン テ キ ス ト 保 存 )
ニ ュ ア ン ス が 消 え る
情 報 が 断 片 化
× 情 報 が 増 え る ほ ど
Mem0
重 要 な 事 実 だ け 保 存
文 脈 · 背 景 情 報 が 消 え や す い
RAG で 必 要 な 情 報 を 検 索
検 索 精 度 が 低 下
( 重 要 事 実 の み )
シ ン プ ル で 軽 量
記 憶 が 細 分 化 し や す い
関 係 性 を グ ラ フ で 保 持
ド メ ン 横 断 に 汎 化 し に く い
要 約 や 重 要 事 実 だ け 保 存
×
関 連 情 報 の 取 り 逃 が し
GraphRAG
複 雑 な 関 連 を 表 現
( 硬 直 的 な オ ン ト ロ ジ ー )
が 発 生
Memora
抽 象 と 詳 細 を 調 和 さ せ て 保 持
研 究 段 階
( 本 技 術 )
多 様 な 手 掛 か り か ら 効 率 的 に 探 索
( 今 後 の 発 展 に 期 待 )
3
Memora の ア ー キ テ ク チ ャ :3 つ の 要 素 で 1 つ の Memory Entry を 構 成
Memora は 「 Memory Content( 何 を 覚 え る か ) 」 と 「 Memory Structure ( ど う 構 造 化 し て ア ク セ ス す る か ) 」 を 分 離 し た 設 計
例 : プ ロ ジ ェ ク ト の 記 憶
Memora の Memory Entry (1 つ の 記 憶 単 位 )
複 数 の 手 掛 か り か ら
実 際 の 出 来 事 ( 時 系 列 で 発 生 )
1 Primary Abstraction ( 主 抽 象 )
*Primary Abstraction
同 じ 記 憶 ヘ ア ク セ ス
4 月 1 日
そ の 記 憶 を 一 意 に 表 す “ 代 表 ラ ベ ル ”
· 記 憶 を 識 別 す る た め の
質 問 : 「 Dave と 合 意 し た ス ケ ジ ュ ー ル は ? 」
Project Orion®
(6~8 話 の 趙 い フ レ ー ズ )
安 定 し た ラ ベ ル
プ ロ ト タ イ プ を
Updated Project Orion timeline agreed by Dave and Sarah
· Memory Value が 更 新 さ れ て
→ Anchor 「 Dave 」 か ら 検 索
4 月 1 日 に 延 期 す る
も 極 力 縄 持 さ れ る
Project Oriona)
こ と で 合 意
ス ケ ジ ュ ー ル 変 更
( 同 じ 記 憶 )
5 月 2 日
2 Memory Value ( 記 憶 の 中 身 : 詳 細 情 報 )
バ イ ロ ッ ト を
関 連 す る す べ て の 詳 細 を 統 合 · 更 新 し 続 け る
Memory Value
5 月 2 日 に 延 期 す る
·4 月 1 日 : プ ロ ト タ イ プ を 4 月 1 日 に 延 期 (Dave と Sarah が 合 意 )
· 実 際 の 詳 細 情 報 を 保 存
質 問 : 「 バ イ ロ ッ ト の 延 期 日 は ? 」
こ と で 合 意
·5 月 2 日 : パ イ ロ ッ ト を 5 月 2 日 に 延 期 (Dave と Sarah が 合 意 )
· 新 し い 出 来 事 が 起 き る た び に
→ Anchor 「 バ イ ロ ッ ト 」 か ら 検 索
·5 月 30 日 :MVP を 5 月 30 日 に 延 期 (Dave と Sarah が 合 意 )
追 記 · 更 新
Project Oriona)
5 月 30 日
MVP を
. Mi@ # : Dave. Sarah, Project Orion7-4
· 過 去 の 文 脈 や 細 部 も 保 持
ス ケ ジ ュ ー ル 変 更
( 同 じ 記 憶 )
5 月 30 日 に 延 期 す る
· 間 連 ド キ ュ メ ン ト 、 決 定 理 由 、 背 景 …..
こ と で 合 意
Cue Anchors
質 問 : 「 MVP の 新 し い 日 付 は ? 」
3 Cue Anchors ( 手 掛 か り の 集 合 )
· 多 様 な 切 り 口 ( 人 物 · 物 事 ·
→ Anchor 「 MVP 」 か ら 検 索
こ の 記 憶 へ 到 達 す る た め の “ 入 口 ” を 多 数 用 意 す る
イ ベ ン ト · ト ピ ッ ク な ど ) で
MVP
Project Oriona)
(Semantic Anchor : 人 物 · イ ベ ン ト · 関 係 · ト ピ ッ ク な ど )
ア ク セ ス 可 能 に す る
ス ケ ジ ュ ー ル 変 更
Dave
Sarah
Project Orion
プ ロ ト タ イ プ パ イ ロ ッ ト
MVP
· ど の 手 掛 か り か ら で も
( 同 じ 記 憶 )
開 発 計 画
ス ケ ジ ュ ー ル 変 更
同 じ 記 憶 に 到 達 で き る
リ リ ー ス 延 期
合 意
入 口 は 違 っ て も 、 到 連 す る 記 憶 は 同 じ
4
人 間 の 記 憶 に 近 い 設 計
5
Policy-guided Retriever ( 探 索 ア ル ゴ リ ズ ム )
人 は 、 い ろ い ろ な 手 掛 か り か ら
Memora は 複 数 の Cue( 手 掛 か り )
Memora は 、 必 要 な 情 報 が 揃 う ま で 探 索 方 針 を 動 的 に 調 整 す る
同 じ 記 憶 を 思 い 出 す
か ら 同 じ 記 憶 ヘ ア ク セ ス で き る た め 、
一 般 的 な RAG
Memora の 採 楽 フ ロ ー
探 索 の イ メ ー ジ (Memory Graph 上 を 移 動 )
「 4 月 1 日 に
人 間 の 記 憶 の よ う に 柔 軟 で 自 然
雙 間
初 期 晚 點
何 が あ っ た ? 」
( 関 連 す る Cue か ら 探 索 開 ぬ )
Memory Entry A
Cue
Cue
Dave 7
Dave
MVP
、 検 索 (1 回 )
関 連 す る Memory Entry を 取 得
O
だ っ け ? 」
→
Memory Entry B
Memory Entry C
4 月 1 日
1
情 報 は 十 分 か ?
探 索 ポ リ シ ー を 調 整
!!
「 Orion の プ ロ ジ ェ ク ト の
結 果 を 取 得
(WVDCue 免 通 訊 / 品 限 り /
Cue
ス ケ ジ ュ ー ル は ? 」
例 間 題 Memory へ 移 館 )
Memory Entry D
同 じ 記 憶
Yes
終 了
十 分 な 情 報 を 取 得
必 要 な 情 報 が 揃 う ま で
「 情 報 が 不 足 し て て て も み て 」
回 答 生 成
複 数 の Cue を 辿 っ て 探 索
6
ベ ン チ マ ー ク 結 果 ( 既 存 手 法 を 上 回 る 性 能 )
7
今 後 の 研 究 構 想 ( 次 世 代 の 記 憶 AI に 向 け て )
LoCoMo ( 長 期 対 話 ベ ン チ マ ー ク )
コ ン テ キ ス ト 効 率 ( ト ー ク ン 使 用 量 )
LLM-as-a-Judge BFffi (E EtE)
フ ル コ ン テ キ ス ト 対 比
MemLoop
Deferred Memory
Group Memory
( 則 話 予 約 約 600 タ ー ン )
( メ ム ル ー プ )
( テ ィ フ ァ ー ド · メ モ リ )
( グ ル ー プ · メ モ リ )
100%
86.39
82.5%
最 大
80%
98%
検 索 や タ ス ク の 失 敗 か ら
十 分 な 文 願 や 情 報 が
複 数 エ ー ジ ェ ン ト 間 で 、
60%
学 習 し 、 記 憶 シ ス テ ム
集 ま る ま で 、 記 憶 化 を
ア ク セ ス 制 御 や 楽 歴 を
40%
雪 個 は
自 体 を 雑 訊 的 に 改 善
保 留 ( 先 送 り ) す る
保 ち な が ら 知 識 を 共 有
20%
削 減
· う ま く い か な か っ た 探 索
· 断 片 的 な 情 報 を す ぐ 保 存 せ ず
· 権 限 管 理 · プ ラ イ バ シ ー 保 護
Memora(P)
フ ル コ ン テ キ ス ト
RAG
フ ル コ ン テ キ ス ト
Memora
· 誤 っ た 記 憶 の 関 連 付 け
· 植 信 度 が 高 ま っ て か ら 統 合
· 記 憶 の 来 歴 ( 由 来 ) を 追 跡
Mem0
( 專 技 術 · 註 LLMN) ( 全 能 甘 読 み 込 み )( 原 費 草 房 (+)
( 全 屋 臣 読 み 込 み )
( 本 次 瓶 )
⇒ 次 回 に 活 か し て 翔 度 向 上
⇒ ノ イ ズ や 誤 記 憶 を 削 減
⇒ チ ー ム で の 協 調 知 識 を 実 現
※LoCoMo の 数 量 は LLM-as-a-Judge 評 価 、 Memora(P) は 強 力 な LLM で プ ロ ン プ ト す る 方 式 の 結 果 。
8
現 状 ま と め
Microsoft Research が 開 発 · 発 表 (2026/6/29 米 国 時 間 )
現 在 は 研 究 段 階
Memora は 、 AI エ ー ジ ェ ン ト が 長 期 に わ た り
-
論 文 (ICML 2026 採 択 )· コ ー ド を 公 開 済 み
Microsoft 365 Coplot な ど の 製 品 へ の
文 脈 を 理 解 し 続 け る た め の 基 盤 技 術 と し て 、
革 新 的 な 長 期 記 憶 ア ー キ テ ク チ ャ と し て 高 い 性 催 を 追 成
搭 載 に つ い て は 記 載 な し
今 後 の 発 展 が 期 待 さ れ る 重 要 な 研 究 で す 。
99
gt : Microsoft Research Blog "Memora: A Harmonic Memory Representation Balancing Abstraction ner(2026/6city]
(2026/6/29) 論 文 :arXiv: 2602.03315 (ICML 2026)
J-F : https://github.com/microsoft/Memora
### : https://www.microsoft.com/en-us/research/blog/memora/ ](20260701_MicrosoftMemora.files/image001.png)
