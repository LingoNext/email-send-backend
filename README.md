> ⚠️ **警告：不要在這裡實作專題，請前往 Emotional-Bot-Backend，此專案僅供學習參考用途！**
## Email Send Backend

這是一個基於 Django 的郵件發送後端服務，支援用戶註冊、登入、驗證碼發送等功能。
- Django 框架
- PostgreSQL 資料庫
- HOPPSCOTCH API 測試工具

### 安裝方式
1. 下載或 clone 此專案：
	```bash
	git clone https://github.com/LingoNext/email-send-backed.git
	```

2. 安裝 PostgreSQL 並建立資料庫：
	- 安裝 [PostgreSQL](https://www.postgresql.org/download/)
	- 開啟 Stack Builder 並安裝附加元件
	- 開啟 pgAdmin 並建立一個資料庫（預設名稱為 `postgres`）與用戶（預設為 `postgres`）
	- 確認主機名稱（預設名稱為`localhost`）和 Port 號（預設名稱為`5432`）
	- 設定密碼，並記下密碼（供後續環境變數使用）
3. 設定環境變數 `DB_PASSWORD` 為你的 PostgreSQL 密碼：
	- Windows PowerShell：
	  ```powershell
	  $env:DB_PASSWORD = "你的密碼"
	  ```
	- 或將其加入系統環境變數
4. 前往[設定應用密碼](https://support.google.com/accounts/answer/185833?hl=zh-Hant)，名稱可以自己取，並修改 `settings.py` 
   ![設定應用密碼](assets/img/set_email_password.png)
    ```python
    EMAIL_HOST_USER = "chen199940@gmail.com" #改為你的信箱
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD') #設定環境變數`EMAIL_PASSWORD`
    ```
    > 應用程式密碼是一個 16 位數密碼，輸入環境變數請移除空格!

5. 進入專案資料夾並建立虛擬環境：
	```bash
    cd email_send_backed
	python -m venv env
	env\Scripts\activate
	```
6. 安裝相依套件：
	```bash
	pip install -r requirements.txt
	```

### 資料庫遷移
```bash
python manage.py migrate
```
![安裝資料表](assets/img/install_apps.png)
### 啟動伺服器
```bash
python manage.py runserver 0.0.0.0:8000
```
![運行資訊](assets/img/server_information.png)
### 完整 API 測試流程

- 驗證碼發送
![測試1](assets/img/test1.png)
![測試2](assets/img/test2.png)
- 註冊
![測試3](assets/img/test3.png)
- 登入
![測試4](assets/img/test4.png)
- 移除帳號
![測試5](assets/img/test5.png)
![測試6](assets/img/test6.png)