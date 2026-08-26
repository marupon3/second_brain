---
created: 2026-04-30
source: https://x.com/ClaudeCode_UT/status/2049770357419299237?s=20
tags:
  - claude
  - skills
---
![[Pasted image 20260823174628.png]]

『海外でバズってるSkillsの記事、全部英語で読みきれない』

『Skills入れたいけど、結局どれを入れればいいか分からなくて放置してる』

これあるあるですよね。情報の海に溺れてしまっている状態で何が正解かわからなくなっています。

[

![画像](https://pbs.twimg.com/media/HHIT_YcbgAA7Kls?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049722760021377024)

Claude Codeを使ってて、こんな経験はありませんか？

- 海外で420万人が読んだSkills記事がバズってるのに、英語で読みきれない
    
- Skills関連の記事をブクマしたけど、どれを入れればいいか分からず放置してる
    
- 周りがAIを使いこなし始めてるのに、自分はまだ毎回ゼロから指示してる焦り
    
- 毎回AIに同じ説明をやり直してる。前回教えたことが消えてる
    

そんな方向けにトッププレイヤーが使っているSKillsをようと別になんと72個整理してみました。オリジナルで作っているSKillsもあるので参考にしてみてください。

AI Builder / CEO のMr. Buzzoni氏が書いた記事が420万ビュー、1.9万ブックマークの大バズ中です。

始める前に2つだけ。

1. この記事を保存して、今週20分だけ時間を確保してください
    
2. Claude Codeを使ってる人にこの記事を共有してください
    

今回はその内容をわかりやすく噛み砕いて、さらにSKILL.mdの中身を直接読んで解説します。

元記事で紹介されているのは67個のSkills。この記事ではそれを日本のビジネス現場向けに4つのカテゴリへ再構成し、さらに独自の組み合わせパック3つと実務スキル2つを加えた72選として紹介します。

元ポストはこちら：

[https://x.com/polydao/status/2044317956893471081](https://x.com/polydao/status/2044317956893471081)

## 

Skillsは「一度教えたら永久に覚える仕組み」

[

![画像](https://pbs.twimg.com/media/HHIUXM1akAApvNG?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723169221808128)

普段のAIチャットは、セッションが終わるとすべてリセットされます。

先週教えた「報告書のフォーマット」も「プレゼンの好み」も消えている。だから毎回ゼロから同じ説明をやり直すことになります。

Skillsはこの問題を根本から解決する仕組みです。

SKILL.mdというファイルに「仕事のやり方」を定義しておくと、Claude Codeが永久にそのルール通りに動きます。手順、制約、テンプレート、具体例。全部1つのファイルに書いておくだけです。

インストールは1行のコマンドだけ。

bash

```bash
claude install @anthropics/skills/pdf
```

これを実行するだけで、PDFの読み取りや結合、分割がいつでも使えるようになります。

入手先やエコシステムの全体像は後半で詳しく解説します。ここからは、あなたの仕事に合うSkillsを4つのカテゴリから見つけていきましょう。

## 

「考える」企画と壁打ち

[

![画像](https://pbs.twimg.com/media/HHIUj_XagAADzmT?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723388944613376)

「考える時間」は、ビジネスの中で最も価値が高い時間です。

ところが多くの人は、企画書のフォーマットを整えたり、過去資料を探したり、下書きを繰り返す「作業」に時間を奪われています。

Skillsのある世界線とない世界線で比較してみましょう。

Before: 企画書を1人で3日かけて書く。壁打ち相手がいない

After: AIと壁打ちして30分で骨子が完成。残りの時間は判断と意思決定に集中

■ Brainstorming (obra/superpowers)

アイデアを投げると、AIが9ステップの構造化プロセスで設計書まで仕上げます。

まず「何を作りたいか」を聞き出し、視覚補助を提案し、質問を投げかけ、複数のアプローチを提示する。設計書が完成したらAI自身がレビューし、さらにあなたにもレビューを求めます。

[

![画像](https://pbs.twimg.com/media/HHIUopUbAAAlxGV?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723468925829120)

このスキルの最も重要なルールは「設計書を承認するまで一切コードを書かない」ということです。

考えがまとまる前に実行に移さない仕組みが最初から組み込まれています。企画や提案のクオリティが、個人の「考える力」ではなく「プロセスの力」で上がるようになります。

正直、これだけでもSkillsを入れる価値があります。

→

[https://github.com/obra/superpowers/tree/main/skills/brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming)

■ Grill Me (mattpocock/skills)

個人的イチオシです。

「これでいいかな」と思った計画をAIに渡すと、考慮漏れを1つずつ質問攻めにしてくれるスキルです。

決定ツリーの分岐を1つずつ解決していく質問インタビュー形式で、各質問には推奨回答も提示されます。答えに詰まったら、AIがドキュメントを直接調べて質問を省略してくれる機能まであります。

イメージとしては「上司に突っ込まれる前に、AIに突っ込んでもらう」です。計画の穴を事前に全部潰せます。

→

[https://github.com/mattpocock/skills/tree/main/grill-me](https://github.com/mattpocock/skills/tree/main/grill-me)

[

![画像](https://pbs.twimg.com/media/HHIUtIjbkAAJ_2O?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723546029756416)

■ Write a PRD (mattpocock/skills)

打ち合わせやチャットのやり取りから、企画書を自動で作成するスキルです。SKILL.mdの中を見ると、わざわざインタビューし直すのではなく、会話の文脈から直接PRDを生成する設計になっています。問題の定義、解決策、必要な機能の一覧、対象外の項目まで構造化された企画書が出力されます。

→

[https://github.com/mattpocock/skills/tree/main/write-a-prd](https://github.com/mattpocock/skills/tree/main/write-a-prd)

■ PRD to Plan (obra/superpowers)

企画書から詳細な実行計画を自動生成するスキルです。タスクを2分から5分の単位に分解し、実際のファイルパスや実行コマンドまで含んだ具体的な計画書として出力します。「何をやるか」だけでなく「どこからどう手をつけるか」まで落とし込めるのがポイントです。

→

[https://github.com/obra/superpowers](https://github.com/obra/superpowers)

■ PRD to Issues (mattpocock/skills)

企画書をタスクチケットに自動変換するスキルです。SKILL.mdでは「垂直スライス」という概念が使われていて、1つのタスクが最初から最後まで一気通貫で完結するように分割されます。各タスクは「人の判断が必要か」「自律で進められるか」も分類されるので、チームへの依頼がしやすくなります。

→

[https://github.com/mattpocock/skills/tree/main/prd-to-issues](https://github.com/mattpocock/skills/tree/main/prd-to-issues)

■ Design an Interface (mattpocock/skills)

画面やシステムの設計案を、AIが3つ以上の根本的に異なるアプローチで同時に生成するスキルです。「最初のアイデアが最良とは限らない」という設計哲学に基づいていて、シンプルさ重視、柔軟性重視、最頻出ユースケース重視など異なる制約で設計を比較できます。企画段階の意思決定を加速させます。

→

[https://github.com/mattpocock/skills/tree/main/design-an-interface](https://github.com/mattpocock/skills/tree/main/design-an-interface)

■ Domain Name Brainstormer (

[skillsmp.com](https://skillsmp.com)

)

サービス名やドメイン名のアイデアを大量に生成してくれるスキルです。ブランディングの壁打ち相手として使えます。思いつかない切り口のネーミング候補が次々出てくるので、新規事業やプロジェクトの立ち上げ時に重宝します。

→

[https://github.com/Microck/ordinary-claude-skills/tree/main/skills_all/domain-name-brainstormer](https://github.com/Microck/ordinary-claude-skills/tree/main/skills_all/domain-name-brainstormer)

■ Idea Mining / YouTube (

[skillsmp.com](https://skillsmp.com)

)

YouTubeからコンテンツのアイデアを自動収集してくるスキルです。競合チャンネルの人気動画や、特定テーマのトレンドを分析して、次に作るべきコンテンツの企画を提案してくれます。YouTube運用をしている人だけでなく、動画マーケティングのリサーチにも使えます。

→

[https://github.com/AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube)

企画と計画ができたら、次は実際に「作る」フェーズです。

## 

「作る」デザインと制作と開発

[

![画像](https://pbs.twimg.com/media/HHIU2rgacAA3prz?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723710031163392)

「作れる」のハードルが下がると、「何を作るか」の判断力こそが差別化になります。

このカテゴリは全72個の中で最もボリュームがあります。デザイン、Web、画像、動画からコード開発まで幅広くカバーしています。

Before: Webサイトのデザインを外注して2週間待つ

After: AIに言葉で指示して、1日で本番品質のデザインが完成

■ Frontend Design (Anthropic公式)

「こんなWebページが欲しい」と言葉で伝えるだけで、プロが作ったような画面が出てきます。

SKILL.mdの設計原則には「AIっぽいありきたりなデザインを避けること」が明示的に書かれています。ダッシュボードやWebアプリなど、本番で使えるレベルのUIを生成します。

デザイナーがいなくても、プロトタイプを自分で作って確認できます。企画段階での意思決定が格段に速くなります。

→

[https://github.com/anthropics/skills/tree/main/skills/frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)

■ Canvas Design (Anthropic公式)

このスキルの面白いところは、いきなり絵を描かないことです。

[

![画像](https://pbs.twimg.com/media/HHIVCHhbwAE6K1M?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049723906530197505)

まず「デザイン哲学マニフェスト」を言語化するところから始まります。「何を伝えたいか」を先に定義してから、PNGやPDFのビジュアルとして表現する2段階プロセスです。

だから「それっぽいけど何を伝えたいか分からない」という成果物にはなりません。SNS素材、ポスター、資料の挿絵を作るときに威力を発揮します。

AIを活用する時って言語化がすごく大事なんですよ。同じ目的だとしても伝える情報の具体性や周辺情報、背景があるだけでかなり品質に影響します。

→

[https://github.com/anthropics/skills/tree/main/skills/canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)

■ Theme Factory (Anthropic公式)

「資料の見た目をプロっぽくしたい」を最も手軽に解決するスキルです。

10種類のプリセットテーマから選ぶか、カスタムで生成するかを選択。カラーパレットとフォントペアリングが全ページに統一適用されます。

色やフォントの選定で悩まなくていい。資料を作るたびに「見た目の統一」に時間を使っていた人は、このスキルだけでも入れる価値があります。

→

[https://github.com/anthropics/skills/tree/main/skills/theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory)

[

![画像](https://pbs.twimg.com/media/HHIVTUZbEAAKJwt?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049724202044035072)

■ Awesome-design (

[skillsmp.com](https://skillsmp.com)

)

デザインのベストプラクティスを集めたスキルです。プロが使う設計パターンやレイアウトの原則を参照できるので、デザインの「なぜこうするのか」が分かるようになります。Frontend DesignやCanvas Designと組み合わせると、デザインの精度がさらに上がります。

→

[https://github.com/VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

■ Image Generator (

[skillsmp.com](https://skillsmp.com)

)

画像生成のプロンプトを最適化し、品質を管理するスキルです。2種類のバリエーションが用意されていて、それぞれ異なる画像生成サービスに対応しています。「何を生成してほしいか」の指示を最も効果的な形に変換してくれるので、生成画像のクオリティが安定します。

→

[https://github.com/kingbootoshi/nano-banana-2-skill](https://github.com/kingbootoshi/nano-banana-2-skill)

■ Local Image Gen (

[skillsmp.com](https://skillsmp.com)

)

クラウドを使わずにローカル環境で画像を生成するスキルです。外部サービスにデータを送りたくない場合や、オフラインで作業したい場合に使えます。機密性の高いプロジェクトのビジュアル作成に向いています。

→

[https://github.com/jezweb/claude-skills/blob/main/plugins/design-assets/skills/ai-image-generator/SKILL.md](https://github.com/jezweb/claude-skills/blob/main/plugins/design-assets/skills/ai-image-generator/SKILL.md)

■ Image Optimizer (

[skillsmp.com](https://skillsmp.com)

)

画像の圧縮、フォーマット変換、リサイズを自動処理するスキルです。Webサイトに載せる画像の最適化や、メール添付用にファイルサイズを落としたいときに便利です。1枚ずつ手作業で処理していた時間がなくなります。

→

[https://mcpmarket.com/tools/skills/image-optimizer](https://mcpmarket.com/tools/skills/image-optimizer)

■ Brand Guidelines (Anthropic公式)

ブランドカラーやフォントをアーティファクトに自動適用するスキルです。SKILL.mdを読むと、これはAnthropicのブランド向けに設計された専用スキルです。自社のブランドガイドラインに書き換えれば、社内資料のデザイン統一に応用できます。

→

[https://github.com/anthropics/skills/tree/main/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)

■ Algorithmic Art (Anthropic公式)

p5.jsを使ってインタラクティブなアート作品を生成するスキルです。パラメータスライダー付きのHTMLビューアーとして出力されるので、数値を変えながらリアルタイムで変化を楽しめます。プログラミング経験がなくてもクリエイティブな実験ができます。

→

[https://github.com/anthropics/skills/tree/main/skills/algorithmic-art](https://github.com/anthropics/skills/tree/main/skills/algorithmic-art)

■ Web Artifacts Builder (Anthropic公式)

(開発者向け) React、TypeScript、Tailwindで複雑なWebアプリをHTMLアーティファクトとして生成するスキルです。

SKILL.mdではshadcn/uiとの連携が組み込まれていて、ルーティングや状態管理にも対応しています。デザインの確認やプロトタイプの高速作成に使えます。

→

[https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder)

■ TDD (mattpocock/skills)

(開発者向け) テストを先に書いてからコードを書く「テスト駆動開発」を自動化するスキルです。

SKILL.mdでは「計画→トレーサー弾→反復→リファクタリング」の4ステップが定義されています。Red-Green-Refactorのループをそのまま実行してくれるので、テストを先に書く文化をAIに組み込めます。

→

[https://github.com/mattpocock/skills/tree/main/tdd](https://github.com/mattpocock/skills/tree/main/tdd)

■ Code Review (obra/superpowers)

(開発者向け) コードレビューの品質を向上させるスキルです。

obra/superpowersでは「レビューを受ける側」と「レビューする側」の2つのスキルに分かれていて、それぞれの観点が構造化されています。レビューの抜け漏れを仕組みで防ぎます。

→

[https://github.com/obra/superpowers](https://github.com/obra/superpowers)

■ Systematic Debugging (obra/superpowers)

(開発者向け) あらゆるバグを4フェーズで体系的に解決するスキルです。

根本原因の調査、パターンの分析、仮説の検証、実装まで段階を踏みます。SKILL.mdでは「3回修正に失敗したらアーキテクチャを見直す」というルールまで設定されていて、場当たり的な修正を防ぐ設計になっています。

→

[https://github.com/obra/superpowers/tree/main/skills/systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging)

■ Superpowers (obra/superpowers)

(開発者向け) 20個のエンジニアリングスキルを一括導入できるメガコレクションです。

Brainstorming、Systematic Debugging、Writing Plansなど、この記事で紹介している複数のスキルがセットで入ります。16.6万スターの巨大リポジトリで、エンジニアリング基盤を一発で構築できます。

→

[https://github.com/obra/superpowers](https://github.com/obra/superpowers)

■ Improve Codebase Architecture (mattpocock/skills)

(開発者向け) コードベースの設計品質を改善するスキルです。

SKILL.mdではADR(設計判断記録)を参照しながら、「浅いモジュールを深いモジュールに変換する」という設計哲学に基づいて改善提案を行います。大規模プロジェクトのリファクタリングに効果を発揮します。

→

[https://github.com/mattpocock/skills/tree/main/improve-codebase-architecture](https://github.com/mattpocock/skills/tree/main/improve-codebase-architecture)

■ QA (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) テスト自動化と品質保証のスキルです。

テストケースの設計から実行、結果の分析まで一貫して処理します。手動テストの工数を大幅に削減できます。

→

[https://github.com/mattpocock/skills/tree/main/qa](https://github.com/mattpocock/skills/tree/main/qa)

■ Triage Issue (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) バグ報告の分類と優先順位付けを自動化するスキルです。

影響範囲の分析と再現手順の整理まで行います。チームのIssue管理が格段に速くなります。

→

[https://github.com/mattpocock/skills/tree/main/triage-issue](https://github.com/mattpocock/skills/tree/main/triage-issue)

■ Auto-Commit Messages (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) 変更内容を分析してコミットメッセージを自動生成するスキルです。

コミットメッセージの書き方がチーム全体で統一されます。「何を変えたか」だけでなく「なぜ変えたか」まで記録する品質が保てます。

→

[https://github.com/anthropics/skills/tree/main/skills/auto-commit](https://github.com/anthropics/skills/tree/main/skills/auto-commit)

■ Change Log Generator (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) コミット履歴から変更履歴を自動生成するスキルです。

リリースノートの作成工数が大幅に減ります。手動でまとめていた変更一覧が、コマンド1つで完成します。

→

[https://github.com/ComposioHQ/awesome-claude-skills/tree/master/changelog-generator](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/changelog-generator)

■ Simplification Cascade (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) 複雑なコードを段階的に簡素化するスキルです。

リファクタリングの判断基準を構造化して適用します。どこから手をつけるべきかの優先順位まで提示してくれます。

→

[https://mcpmarket.com/tools/skills/simplification-cascades-1](https://mcpmarket.com/tools/skills/simplification-cascades-1)

■ React Best Practices (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Reactのベストプラクティスをコードに自動適用するスキルです。

コンポーネント設計やパフォーマンス最適化のパターンが組み込まれています。React開発の品質を底上げできます。

ちなみに開発文脈以外でも「ベストプラクティス」を見つけてきてくれるskillsは公開されているものが多いので気になる方は調べてみてください。

→

[https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices)

■ File Search (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) コードベース内のファイル検索を最適化するスキルです。

大規模リポジトリでも目的のファイルを素早く特定します。「あのファイルどこだっけ」の時間がなくなります。

→

[https://github.com/massgen/massgen](https://github.com/massgen/massgen)

■ Context Optimization (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Claude Codeのコンテキスト管理を最適化するスキルです。

長いセッションでもパフォーマンスを維持する工夫が組み込まれています。大規模プロジェクトでの作業効率が上がります。

→

[https://github.com/muratcankoylan/agent-skills-for-context-engineering](https://github.com/muratcankoylan/agent-skills-for-context-engineering)

■ Migrate to Shoehorn (mattpocock/skills)

(開発者向け) フレームワーク移行を支援するスキルです。

移行計画の策定から段階的な実行までガイドします。移行に伴うリスクを最小化しながら進められます。

→

[https://github.com/mattpocock/skills/tree/main/migrate-to-shoehorn](https://github.com/mattpocock/skills/tree/main/migrate-to-shoehorn)

■ Scaffold Exercises (mattpocock/skills)

(開発者向け) コード演習の問題を自動生成するスキルです。

学習用の課題やチュートリアルの素材を素早く作れます。技術研修の準備にも使えます。

→

[https://github.com/mattpocock/skills/tree/main/scaffold-exercises](https://github.com/mattpocock/skills/tree/main/scaffold-exercises)

■ Request Refactor Plan (mattpocock/skills)

(開発者向け) リファクタリング計画を策定するスキルです。

現在はdeprecatedで、diagnoseやzoom-outに置き換えられています。既存プロジェクトで使っている場合は移行を検討してください。

→

[https://github.com/mattpocock/skills/tree/main/request-refactor-plan](https://github.com/mattpocock/skills/tree/main/request-refactor-plan)

■ Stripe Integration (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Stripeの決済機能を実装する支援スキルです。

APIの接続から決済フローの構築までガイドします。Stripeを使った決済導入の工数を大幅に短縮できます。

→

[https://github.com/wshobson/agents/tree/main/plugins/payment-processing/skills/stripe-integration](https://github.com/wshobson/agents/tree/main/plugins/payment-processing/skills/stripe-integration)

■ Setup Pre-Commit (mattpocock/skills)

(開発者向け) コミット前のチェックを自動設定するスキルです。

コードの品質ゲートを簡単に導入できます。チーム全体のコード品質を仕組みで担保します。

→

[https://github.com/mattpocock/skills/tree/main/setup-pre-commit](https://github.com/mattpocock/skills/tree/main/setup-pre-commit)

■ Git Guardrails (mattpocock/skills)

(開発者向け) Gitの安全ルールを設定するスキルです。

危険なコマンドの防止や、ブランチ保護のルールを自動構築します。チーム開発での事故防止に直結します。

→

[https://github.com/mattpocock/skills/tree/main/git-guardrails-claude-code](https://github.com/mattpocock/skills/tree/main/git-guardrails-claude-code)

■ Dependency Auditor (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) 依存パッケージのセキュリティ監査を自動化するスキルです。

脆弱性のあるパッケージを検出して対処方法を提案します。セキュリティリスクを早期に発見できます。

→

[https://github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

■ Git Work Trees (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) 複数のブランチを並列で作業するための環境構築を自動化するスキルです。

ブランチ切り替えのコストを最小化します。複数機能の同時開発が格段にやりやすくなります。

→

[https://skillsmp.com](https://skillsmp.com/)

■ Remotion Best Practices (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Remotionでの動画制作のベストプラクティスを適用するスキルです。

プログラマブルな動画制作の品質を上げたい人向けです。コードで動画を作る際のパターンが整理されています。

RemotionやHyperFrameなど、プログラミング的に動画を作成していく流れは今後絶対に加速するのでぜひこの際に押さえておきたいですね❗️

→

[https://github.com/remotion-dev/remotion](https://github.com/remotion-dev/remotion)

■ Emotion (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) CSS-in-JSのスタイリングを効率化するスキルです。

Reactアプリのスタイリングを統一的に管理できます。デザインシステムとの連携にも対応しています。

→

[https://github.com/wilwaldon/Claude-Code-Video-Toolkit](https://github.com/wilwaldon/Claude-Code-Video-Toolkit)

作ったものを世に出すには、「調べる」と「書く」のプロセスがあります。

## 

「調べる・書く」リサーチと文書

[

![画像](https://pbs.twimg.com/media/HHIWhyYa8AAsz3Y?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049725550122692608)

「調べて書く」はほぼ全てのビジネスパーソンが毎日やっていることです。

この時間が半分になったら、影響は計り知れません。

Before: リサーチに1日、執筆に1日。合計2日

After: AIがリサーチを整理して、ドラフトまで共同作成。半日で完成

■ Doc Co-Authoring (Anthropic公式)

提案書や企画書をAIと一緒に書くスキルです。

3段階のプロセスが組み込まれています。

まずAIが「何を書くべきか」の情報を収集する。次にセクションごとにドラフトを作成する。

そして最後に、別のセッションを立ち上げて「読者として読んだとき分かりにくい箇所はないか」を自動チェックします。

→

[https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)

[

![画像](https://pbs.twimg.com/media/HHIWnnBaoAAcuI3?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049725650152628224)

この「読者テスト」が地味にすごい。1人で書いて1人で校正していた作業が「AIと共同作成してAIが読者テスト」に変わります。

ちなみにこの設計自体は「ハーネス」の考えも近く、役割ごとに責務を分けてそれぞれのアウトプットを高品質化するという観点では共通の考えです。ビジネス分野においても、エージェントハーネスはすごく重要なので今後解説していきます。

■ Edit Article (mattpocock/skills)

文章の「磨き込み」を任せるスキルです。

文法チェックではありません。SKILL.mdの中身を読むと、記事全体を「情報の依存関係グラフ」として分析する仕組みになっています。どの情報がどの情報の前に必要かを整理して、読み手にとって最も理解しやすい順序に再構成します。

その上で各段落を短く明確に書き直す。1段落あたり最大240文字というルールまで設定されています。論点を研ぎ澄ませるレベルの構造的な編集です。

→

[https://github.com/mattpocock/skills/tree/main/edit-article](https://github.com/mattpocock/skills/tree/main/edit-article)

■ Content Researcher (

[skillsmp.com](https://skillsmp.com)

)

テーマを渡すと、リサーチ結果を構造化して整理してくれるスキルです。関連する情報源を探し、要点を抽出し、テーマ別に分類して出力します。企画書や提案書のリサーチ工程を丸ごと任せられます。

→

[https://github.com/ComposioHQ/awesome-claude-skills/blob/master/content-research-writer/SKILL.md](https://github.com/ComposioHQ/awesome-claude-skills/blob/master/content-research-writer/SKILL.md)

■ Obsidian Vault (mattpocock/skills)

Obsidianと連携して知識を蓄積・検索するスキルです。SKILL.mdではwikilinks記法でノート同士をリンクし、Index Noteで関連トピックをまとめるフラット構造が定義されています。Obsidian創設者のKepano氏が作った派生版もあり、知識管理ツールとしての活用が広がっています。

→

[https://github.com/mattpocock/skills/tree/main/obsidian-vault](https://github.com/mattpocock/skills/tree/main/obsidian-vault)

■ Claude SEO (

[skillsmp.com](https://skillsmp.com)

)

SEO最適化の分析と改善提案を行うスキルです。タイトルやメタディスクリプションの最適化、キーワード配置の提案、コンテンツの構造改善まで対応します。ブログやWebサイトの検索順位を改善したい人向けです。

→

[https://github.com/AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)

■ Ubiquitous Language (mattpocock/skills)

チーム内の用語を統一して定義するスキルです。「同じものを人によって違う名前で呼んでいる」問題を解決します。用語集を自動生成し、ドキュメント全体で用語の揺れをなくします。大人数のプロジェクトで特に効果があります。

→

[https://github.com/mattpocock/skills/tree/main/ubiquitous-language](https://github.com/mattpocock/skills/tree/main/ubiquitous-language)

■ API Documentation Generator (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) APIドキュメントを自動生成するスキルです。コードからエンドポイント、リクエスト/レスポンスの仕様書を生成し、使用例まで付与します。

→

[https://github.com/ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)

■ Marketing Skills (

[skillsmp.com](https://skillsmp.com)

)

マーケティング施策の設計と分析を支援するスキルです。ターゲット設定、メッセージング、チャネル選定の整理から効果測定のフレームワークまで、マーケティングの一連のプロセスをカバーします。

→

[https://github.com/coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)

■ Custom YT Search (

[skillsmp.com](https://skillsmp.com)

)

YouTube動画の高度な検索と分析を行うスキルです。特定のキーワードやチャンネルに絞った動画のトレンド分析ができます。コンテンツマーケティングのリサーチや競合調査に使えます。

→

[https://github.com/ZeroPointRepo/youtube-skills/blob/main/README.md](https://github.com/ZeroPointRepo/youtube-skills/blob/main/README.md)

■ Firecrawl (

[skillsmp.com](https://skillsmp.com)

)

Webサイトからデータを自動抽出するスキルです。複数ページにまたがる情報をまとめて取得し、構造化されたデータとして出力します。手動でのコピペ作業が不要になります。

→

[https://github.com/mendableai/firecrawl](https://github.com/mendableai/firecrawl)

最後は、日常の繰り返し業務を自動化するSkillsです。

## 

「回す」業務とドキュメント

[

![画像](https://pbs.twimg.com/media/HHIXBS8bAAAkH8E?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049726091439570944)

毎月、毎週繰り返す「作業」こそ、Skillsの最大の効果が出る場所です。

作業をAIに定義として渡すことで、あなたは「判断」に集中できるようになります。

Before: 請求書50枚を手入力で15時間。確認に3時間

After: フォルダに入れて15分で全件処理。計算不整合だけ手動確認

■ PPTX (Anthropic公式)

「こんなプレゼンを作って」と指示すると、PowerPointファイルが自動生成されます。

既存のPPTXから内容をテキストとして取り出すこともできるので、過去資料のリメイクにも使えます。生成後は実際のスライド画像を見て確認できるので、出来上がりを目で見て調整可能です。

プレゼン資料作成にかかる時間が劇的に変わります。

→

[https://github.com/anthropics/skills/tree/main/skills/pptx](https://github.com/anthropics/skills/tree/main/skills/pptx)

■ XLSX (Anthropic公式)

Excelファイルのデータ整理、グラフ作成、数式の自動化をAIが代行します。

[

![画像](https://pbs.twimg.com/media/HHIXH8ta8AAewjE?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049726205730156544)

「この列を集計して」「このデータからグラフを作って」という指示で処理が完了します。さらに数式の再計算機能があるので、計算結果が正しいかどうかを自動検証プログラムでチェックしてくれます。

普通にExcel作業をしてる人なら全員恩恵がある、直球のスキルです。

→

[https://github.com/anthropics/skills/tree/main/skills/xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx)

■ PDF (Anthropic公式)

PDFの操作をワンストップで自動化するスキルです。

読み取り、テキスト抽出、複数ファイルの結合、ページの分割。文字が画像になっているPDFのテキスト化やパスワード付き暗号化まで全部対応しています。

ビジネスでPDFを扱わない人はほぼいないので、入れておいて損はありません。

→

[https://github.com/anthropics/skills/tree/main/skills/pdf](https://github.com/anthropics/skills/tree/main/skills/pdf)

■ DOCX (Anthropic公式)

Word文書の作成と編集を自動化するスキルです。SKILL.mdを見ると、新規作成はJavaScriptのライブラリで生成、既存文書の修正はXMLを直接編集する2つのアプローチが使い分けられています。書式設定やスタイルの適用まで自動化できます。

→

[https://github.com/anthropics/skills/tree/main/skills/docx](https://github.com/anthropics/skills/tree/main/skills/docx)

■ Excel MCP Server (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Excelをサーバー経由で操作するスキルです。MCPプロトコルを使ってExcelデータにプログラムからアクセスし、複雑なデータ処理パイプラインを構築できます。

→

[https://github.com/haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server)

■ GWS (

[skillsmp.com](https://skillsmp.com)

)

Googleスプレッドシート、ドキュメント、スライドと連携するスキルです。Google Workspaceを日常的に使っている人は、Office系スキルの代わりにこちらを導入すると業務フローに合います。

→

[https://github.com/googleworkspace/cli](https://github.com/googleworkspace/cli)

■ NotebookLM Integration (

[skillsmp.com](https://skillsmp.com)

)

GoogleのNotebookLMと連携してリサーチを強化するスキルです。NotebookLMに蓄積した情報源をClaude Codeから参照し、より深いリサーチと分析が可能になります。

→

[https://github.com/PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill)

■ Lead Research Assistant (

[skillsmp.com](https://skillsmp.com)

)

見込み客の企業調査を自動化するスキルです。企業名を入力すると、事業内容、最新ニュース、競合状況などを自動で調査してレポートにまとめます。営業の商談準備にかかる時間を大幅に短縮できます。

→

[https://github.com/ComposioHQ/awesome-claude-skills/blob/master/lead-research-assistant/SKILL.md](https://github.com/ComposioHQ/awesome-claude-skills/blob/master/lead-research-assistant/SKILL.md)

■ GitHub Triage (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) GitHubのIssueを自動分類して優先順位を付けるスキルです。バグ報告の内容を分析し、影響範囲と緊急度を判定します。

→

[https://github.com/mattpocock/skills/tree/main/github-triage](https://github.com/mattpocock/skills/tree/main/github-triage)

■ Stochastic Multi-Agent Consensus (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) 複数のAIモデルに同じ問題を解かせ、合意形成のプロセスで最適な解を導くスキルです。単一モデルでは見落としがちな観点を多角的にカバーします。

→

[https://skillsmp.com](https://skillsmp.com/)

■ Model-chat / Debate (

[skillsmp.com](https://skillsmp.com)

)

AIモデル同士を対話させて多角的に分析するスキルです。異なる立場からの議論をシミュレーションできるので、意思決定の前にメリットとデメリットを網羅的に洗い出せます。開発者以外でも、戦略立案の場面で使えます。

→

[https://skillsmp.com](https://skillsmp.com/)

■ Playwright CLI (

[skillsmp.com](https://skillsmp.com)

)

(開発者向け) Webブラウザの自動操作を行うスキルです。Webアプリのテスト自動化やスクレイピングに使います。

→

[https://github.com/microsoft/playwright](https://github.com/microsoft/playwright)

## 

Skillsは4つの場所で手に入る

[

![画像](https://pbs.twimg.com/media/HHIXP6-bAAAVMrJ?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049726342703546368)

Skillsは自分で作るだけではありません。すでに世界中で開発・公開されています。

■ Anthropic公式 (

[https://github.com/anthropics/skills](https://github.com/anthropics/skills)

)

12.1万スターのリポジトリで、ドキュメント生成やデザインの基本スキルを公開中です。この記事で紹介したPDF、XLSX、PPTXなどはすべてここにあります。

■ 個人開発者

Matt Pocock氏のリポジトリ (

[https://github.com/mattpocock/skills](https://github.com/mattpocock/skills)

) は1.65万スター。Grill MeやEdit Articleなど、実務に直結するスキルが揃っています。

obra/superpowers (

[https://github.com/obra/superpowers](https://github.com/obra/superpowers)

) は16.6万スターの巨大コレクション。Brainstormingをはじめとする強力なスキルが入っています。

■ 企業参入

Microsoft、Sentry、Cloudflare、Trail of Bitsなど、大手テック企業もSkillsの開発に参入しています。企業が作るスキルは、そのプロダクトとの連携に最適化されています。

■ マーケットプレイス

SkillsMP (

[https://skillsmp.com](https://skillsmp.com/)

) では6.6万以上のSkillsが公開中。検索してインストールするだけです。

Mr. Buzzoni氏が別記事で調査した結果では、1,116スキル、500以上のリポジトリ、200人以上の作者が確認されています。正直、このスピードは驚きます。

ただし注意点もあります。SKillsは簡単に配布しやすく非公式のものはGitHubなど経由でサクッと公開・インストールできるのでセキュリティリスクも考慮が必要です。不用意にあまり広まっていないスキルを入れまくるのは危険が伴うので、導入前に確認は怠らないように癖付けましょう。

## 

独自スキルを5つ無料公開

[

![画像](https://pbs.twimg.com/media/HHIXrnSa4AAIK-E?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049726818455052288)

ここからは、元記事にはなかったスキルを紹介します。

独自に用意したSkillsを2つと、複数のSkillsを組み合わせた業務パターン別のワークフローパックを3つ、紹介します。

まずは、ここまで紹介してきたSkillsを連携させて「本当に業務が変わる」使い方を3つ紹介します。

■ 企画壁打ちパック

アイデアを投げるだけで、壁打ち→検証→企画書まで一気に完成させるワークフローです。

Brainstormingでアイデアを構造化し、Grill Meで計画の穴を潰し、Write a PRDで企画書にまとめる。3つのスキルを順番に使うだけで、1人で3日かけていた企画書が半日で完成します。

以下のSKILL.mdをコピーして planning-sprint/SKILL.md として保存すれば使えます。

markdown

```markdown
---
name: planning-sprint
description: アイデアを企画書に変換する一気通貫ワークフロー。壁打ち、検証、企画書作成の3ステップを順に実行する。企画や提案の立案時に使用。
---
# 企画壁打ちパック
アイデアを投げると、壁打ち→検証→企画書の3ステップで完成させます。
## 前提スキル
- Brainstorming (@obra/superpowers)
- Grill Me (@mattpocock/skills)
- to-prd (@mattpocock/skills)
## ワークフロー
1. Brainstormingを起動し、アイデアを構造化する。設計書が承認されるまで次に進まない
2. Grill Meで設計書を検証する。考慮漏れを1つずつ質問で潰す
3. to-prdで検証済みの設計を企画書に変換する
## ポイント
- 3つのスキルを順番に呼び出すだけ
- 途中で方向転換したらステップ1に戻る
- 企画の品質が「個人の思考力」ではなく「プロセスの力」で上がる
```

■ ドキュメント一括処理パック

PDF、Word、Excelが混在するフォルダを渡すだけで、中身を自動で読み取って整理するワークフローです。

取引先から届いた見積書、仕様書、価格表。形式がバラバラでも1つのフォルダに入れて「全部読み取って比較表にまとめて」と指示するだけで処理が完了します。

markdown

```markdown
---
name: document-processor
description: PDF、Word、Excelの混在ファイルを一括で読み取り・整理・統合する。書類整理やデータ抽出の場面で使用。
---
# ドキュメント一括処理パック
複数形式のファイルをフォルダに入れるだけで、中身を自動処理します。
## 前提スキル
- PDF (@anthropics/skills)
- DOCX (@anthropics/skills)
- XLSX (@anthropics/skills)
## ワークフロー
1. 処理したいファイルを1つのフォルダにまとめる
2. 「このフォルダの書類を全部読み取って整理して」と指示する
3. AIがファイル形式を自動判定し、それぞれに適した方法で処理する
## 処理方法
- PDF → テキスト抽出。画像PDFはOCR処理
- Word → 本文と書式の読み取り
- Excel → データ抽出。数式は再計算して検証
## ポイント
- ファイル形式を気にせずフォルダに入れるだけ
- Excelの数式は再計算検証するので計算ミスも検出可能
- 抽出結果を比較表や統合レポートとして出力できる
```

■ リサーチ→執筆パック

テーマを投げるだけで、調査、構成、執筆、校正まで一気に完成させるワークフローです。

Doc Co-Authoringで情報収集からドラフト作成、読者テストまで実施。その後Edit Articleで文章全体の構造を最適化します。「調べて書いて直す」が半日で終わります。

markdown

```markdown
---
name: research-to-writing
description: テーマ設定から完成原稿までを一気通貫で処理する。情報収集、構造化ドラフト、構造校正の3ステップ。企画書、提案書、記事の作成に使用。
---
# リサーチ→執筆パック
テーマを投げるだけで、調査・執筆・校正まで一気に完成させます。
## 前提スキル
- Doc Co-Authoring (@anthropics/skills)
- Edit Article (@mattpocock/skills)
## ワークフロー
1. テーマと目的を伝える。AIが調べるべきことを整理する
2. Doc Co-Authoringでセクション構成を提案し、ドラフトを共同作成する。最後に読者テストで分かりにくい箇所を自動指摘
3. Edit Articleでドラフト全体の情報依存関係を分析し、最も理解しやすい順序に再構成する
## ポイント
- Doc Co-Authoringの読者テストで客観フィードバックが入る
- Edit Articleは文法チェッカーではなく構造の編集者。論点の順序を最適化する
- 2つを順番に使うだけで「調べて書いて直す」が半日で終わる
```

さらに、私たちが実務で使っているスキルを2つ公開します。

■ Meeting Automation (/mtg-notes)

会議の録画やテキストを渡すだけで、議事録、TODO、次回アジェンダが15分で完成するスキルです。

Before: 議事録作成に1件30分から40分。週5件で週3時間。TODOの漏れが月2回

After: 1件15分で完了 (確認と修正のみ)。週1.25時間。TODO自動抽出で漏れゼロ

[

![画像](https://pbs.twimg.com/media/HHIco_ba8AAv8jd?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049732270953787392)

特徴は導入ハードルの低さです。テキスト入力だけでも動くので、API契約なしで今日から試せます。

tl;dvやCircleback MCPと連携すれば、会議の録画からの自動取得も可能です。team.mdにメンバー情報を入れておくだけで、話者の推定やTODO担当の割り当て精度が上がります。

議事録のフォーマット、TODO抽出ルール、会議タイプ別テンプレートも同梱されています。

議事録を書いている時間は、本来あなたの判断に使える時間です。

■ Invoice Reader (/read-invoices)

請求書PDFをフォルダに入れるだけで、構造化されたCSVと計算検証レポートが15分で完成するスキルです。

Before: 月50枚で15時間から20時間の手入力。転記ミスが月2件から5件

After: 15分で全件完了。計算検証で不整合を自動検出

[

![画像](https://pbs.twimg.com/media/HHIcutlbAAAllRv?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049732369243111424)

このスキルの設計で最も重要なのは「計算はAI任せにしない」ところです。

品目の合計が小計と一致するか、小計に税を足した額が請求額と一致するか。こうした計算検証はAIではなく自動検証プログラムで厳密に実行します。

テキストベースのPDFはClaude単体で処理。画像やスキャンされたPDFはGeminiのOCRを使う2段構えです。GeminiのAPIキーがなくても、テキストPDFだけなら今日から使えます。

処理済みの請求書は confirmed と flagged に自動振り分けされます。異常が検出されたデータだけ手動で確認すればOKです。

作業をAIに渡し、判断に集中する。まさにSkillsの本質を体現したスキルです。

## 

Skillsの導入はメタスキルから

[

![画像](https://pbs.twimg.com/media/HHIc0YMbYAERd6b?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049732466580348929)

72個もあると「どこから手をつければいいか分からない」となりがちです。

3つのステップで始めましょう。

■ メタスキルを入れる

まずは「Skillsを探す・作る」能力そのものを手に入れます。

- Skill Creator — Anthropic公式のスキル作成ツールです。SKILL.mdでは、新規作成だけでなく既存スキルの改善やパフォーマンス評価のループまで定義されています。トリガー説明文の最適化機能もあり、スキルが適切なタイミングで呼び出されるようにチューニングできます (
    
    [https://github.com/anthropics/skills/tree/main/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
    
    )
    
- Write a Skill — スキルの書き方を教えるスキルです。Matt Pocock版のSKILL.mdには、スキルの構造、descriptionの書き方、いつファイルを分割すべきか、スクリプトを追加すべきかの判断基準まで整理されています。「descriptionはAIがスキルを選ぶ唯一の手がかり」という設計原則が特に重要です (
    
    [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills)
    
    )
    
- Find Skills — 自分に合ったSkillsを検索して発見するスキルです。キーワードやユースケースからマッチするスキルを見つけてくれます。まずこれを入れておけば「こんなスキルある？」とAIに聞くだけで探してもらえます (
    
    [https://skillsmp.com](https://skillsmp.com/)
    
    )
    

この3つを入れるだけで「自分の仕事に合うSkillsを探してきて」「こんなスキルを作って」とAIに頼めるようになります。

■ 自分の仕事で最も時間を使っている作業に合うスキルを1つ選ぶ

いきなり10個入れる必要はありません。

個人的には、まず自分が毎日繰り返してる作業を1つだけSkillsにすることから始めるのがおすすめです。

[

![画像](https://pbs.twimg.com/media/HHIc8wAaUAEilrd?format=jpg&name=small)





](https://x.com/ClaudeCode_UT/article/2049770357419299237/media/2049732610411352065)

- 企画や計画が多い人 → Brainstorming + Grill Me (または企画壁打ちパック)
    
- 資料作成が多い人 → PPTX + Theme Factory
    
- 文書作成が多い人 → Doc Co-Authoring (またはリサーチ→執筆パック)
    
- データ処理が多い人 → XLSX
    
- 書類整理が多い人 → ドキュメント一括処理パック
    

■ 使って、直して、育てる

Skillsは入れて終わりではありません。

SKILL.mdの中身は自由に編集できます。自分の業務に合わせてルールを追加したり、テンプレートを変えたりして育てていくものです。使い込むほど、あなたの仕事に最適化されていきます。

## 

まとめ

- Skillsは「一度教えたら永久に覚える仕組み」。毎回ゼロから説明する時代は終わった
    
- 元記事の67個を日本のビジネス現場向けに再構成し、独自5つを加えた72選
    
- Anthropic公式からコミュニティまで、エコシステムは1,116スキル規模に成長中
    
- 注目スキル10個はSKILL.mdの中身を直接読んだファクトベースの解説
    
- 組み合わせパック3個 (企画壁打ち、ドキュメント一括処理、リサーチ→執筆) はここだけのオリジナル
    
- 独自スキル2個 (会議記録と請求書処理) を無料公開。実務で使っているものをそのまま提供
    
- Skillsの本質は「作業をAIに定義として渡す」仕組み。差別化の源泉は判断と思想にある