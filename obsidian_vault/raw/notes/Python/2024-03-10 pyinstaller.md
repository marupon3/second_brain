---
メモ: 2024-03-10
source: OneNote
作成時刻: 13:56
---

# pyinstaller

pyinstaller
--onefile --windowed --hidden-import=processing --hidden-import=outlook
--add-data "master/master1.csv;master/" --add-data
"master/master2.csv;master/" --add-data
"templates/index.html;templates/" --add-data "templates/result.html;templates/"
main.py
exe化ファイル構成
"config.json",
"config.json"
"main.py",
"main.py"
"outlook.py",
"outlook.py"
"processing.py",
"processing.py"
"master/master1.csv",
"master1.csv"
"master/master2.csv",
"master2.csv"
"templates/index.html",
"index.html"
"templates/result.html",
"result.html”
