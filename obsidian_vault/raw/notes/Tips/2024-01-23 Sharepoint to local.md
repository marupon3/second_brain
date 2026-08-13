---
メモ: 2024-01-23
source: OneNote
---

# Sharepoint to local

火曜日
4:40

<!-- 変換時の注記: OneNote由来の改行を括弧深さ/構文解析で自動復元しました。インデントはOneNote側で失われている場合があり保証されません。実行前に必ず目視確認してください（要確認）。 -->

```python
from shareplum import Office365
from shareplum.site import Version
from shareplum.site import SharePlumSite
import os
# SharePointへの接続情報を設定
sharepoint_url = "<https://your_sharepoint_site_url>"
username = "your_username"
password = "your_password"
# SharePointに接続
authcookie = Office365(sharepoint_url, username=username, password=password).GetCookies()
site = SharePlumSite(sharepoint_url, authcookie=authcookie)
#
ローカルファイルとSharePoint上のパスを指定
local_file_path = "C:\\path\\to\\your\\local\\file.txt"
sharepoint_folder_path
= "/Shared Documents/FolderName" # ファイルをコピー with open(local_file_path, "rb") as file:
    file_name = os.path.basename(local_file_path)
    file_content = file.read()
    site.upload_file(file_content, file_name, sharepoint_folder_path)
from shareplum import Office365
from shareplum.site import Version
from shareplum.site import SharePlumSite
import os
# SharePointへの接続情報を設定
sharepoint_url = "<https://your_sharepoint_site_url>"
username = "your_username"
password = "your_password"
# SharePointに接続
authcookie = Office365(sharepoint_url, username=username, password=password).GetCookies()
site = SharePlumSite(sharepoint_url, authcookie=authcookie)
#
SharePointのファイルパスとローカルの保存先パスを指定
sharepoint_file_path = "/Shared Documents/FolderName/FileName.txt"
local_save_path = "C:\\path\\to\\save\\file.txt"
#
SharePointのファイルをダウンロードしてローカルに保存
file_contents = site.get_file(sharepoint_file_path)
with open(local_save_path, "wb") as file:
    file.write(file_contents)
```
