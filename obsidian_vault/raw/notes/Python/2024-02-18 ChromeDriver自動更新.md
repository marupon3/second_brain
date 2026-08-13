---
メモ: 2024-02-18
source: OneNote
作成時刻: 17:40
---

# ChromeDriver自動更新

from selenium

<!-- 変換時の注記: OneNote由来の改行を括弧深さ/構文解析で自動復元しました。インデントはOneNote側で失われている場合があり保証されません。実行前に必ず目視確認してください（要確認）。 -->

```python
import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
ドライバーのインストール場所
C:\Users\marupon\.wdm\drivers\chromedriver\win64\121.0.6167.184\chromedriver-win32
```
