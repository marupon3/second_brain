---
created: 2026-02-22
source: Android
作成時刻: 15:49
---

# Android_github使い方

Windows側の操作手順を示します。
Windows ローカルから pull → push する手順
Step 1: ローカルの変更を確認・退避
PowerShell で実行：
# プロジェクトフォルダに移動
cd
C:\path\to\PediaDose
# 現在の状態を確認
git status
ローカルに変更がある場合 →
stash で退避：
git stash push
-m "ローカルの変更を退避"
ローカルに変更がない場合 →
そのまま次へ。
Step 2: リモートの最新を取得
# ブランチを指定してフェッチ
git fetch origin
claude/update-android-build-config-Jc4EH
#
ローカルブランチに切り替え（または作成）
git checkout
claude/update-android-build-config-Jc4EH
# リモートの最新を取り込む
git pull origin
claude/update-android-build-config-Jc4EH
Step 3: stash を元に戻す（退避した場合のみ）
git stash pop
コンフリクトが出た場合：
#
コンフリクトしたファイルを確認
git status
# 解決後にステージング
git add .
git stash drop
Step 4: Windows 側で変更を加えて push
# 変更をステージング・コミット
git add .
git commit -m
"コミットメッセージ"
# push
git push -u
origin claude/update-android-build-config-Jc4EH
＊＊＊
現在のリモート状態（保存済み）
ブランチ:
claude/update-android-build-config-Jc4EH
最新コミット: 53636fe
内容: PediaDose
v1.0 全アーキテクチャ（37ファイル、2502行）
