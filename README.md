# Email Send Backend

> **警告：不要在這裡實作專題，請前往 English-Learning-Assistant-Backend ，此專案僅供學習參考用途！**

這是一個基於 Django 的郵件發送後端服務，支援用戶註冊、登入、驗證碼發送等功能。

## 目錄

- [Email Send Backend](#email-send-backend)
	- [目錄](#目錄)
	- [技術棧](#技術棧)
	- [功能特色](#功能特色)
	- [安裝方式](#安裝方式)
		- [1. 下載專案](#1-下載專案)
		- [2. 安裝 PostgreSQL](#2-安裝-postgresql)
		- [3. 設定環境變數](#3-設定環境變數)
		- [4. 設定 Gmail 應用密碼](#4-設定-gmail-應用密碼)
		- [5. 建立虛擬環境](#5-建立虛擬環境)
		- [6. 安裝相依套件](#6-安裝相依套件)
	- [資料庫設定](#資料庫設定)
	- [啟動服務](#啟動服務)
	- [API 文檔](#api-文檔)
		- [基礎信息](#基礎信息)
		- [API 端點](#api-端點)
			- [1. 發送驗證碼](#1-發送驗證碼)
			- [2. 用戶註冊](#2-用戶註冊)
			- [3. 用戶登入](#3-用戶登入)
			- [4. 刪除帳號](#4-刪除帳號)
	- [完整測試流程](#完整測試流程)
		- [1. 驗證碼發送測試](#1-驗證碼發送測試)
		- [2. 用戶註冊測試](#2-用戶註冊測試)
		- [3. 用戶登入測試](#3-用戶登入測試)
		- [4. 帳號刪除測試](#4-帳號刪除測試)
	- [注意事項](#注意事項)
		- [安全性提醒](#安全性提醒)
		- [環境變數檢查清單](#環境變數檢查清單)

## 技術棧

- **後端框架**: Django 5.2.6
- **資料庫**: PostgreSQL
- **API 框架**: Django REST Framework
- **郵件服務**: Gmail SMTP
- **認證方式**: Token Authentication
- **API 測試工具**: HOPPSCOTCH

## 功能特色

- 郵件驗證碼發送
- 用戶註冊與登入
- Token 基礎認證
- 帳號刪除功能
- 安全密碼驗證
- 驗證碼過期機制（5分鐘）

## 安裝方式

### 1. 下載專案
下載或 clone 此專案：
```bash
git clone https://github.com/LingoNext/email-send-backend.git
cd email-send-backend
```

### 2. 安裝 PostgreSQL

安裝並設定 PostgreSQL 資料庫：
- 下載並安裝 [PostgreSQL](https://www.postgresql.org/download/)
- 開啟 Stack Builder 並安裝附加元件
- 開啟 pgAdmin 並建立資料庫：
  - 資料庫名稱：`email_send_db`
  - 用戶名稱：`postgres`
  - 主機名稱：`localhost`
  - Port 號：`5432`
- 設定密碼，並記住此密碼（後續設定環境變數使用）

### 3. 設定環境變數

設定資料庫密碼環境變數：
```powershell
# Windows PowerShell
$env:DB_PASSWORD = "你的PostgreSQL密碼"
```
> **提示**: 建議將環境變數加入系統環境變數，避免每次重啟都要重新設定

### 4. 設定 Gmail 應用密碼

1. 前往 [Google 帳戶設定應用密碼](https://support.google.com/accounts/answer/185833?hl=zh-Hant)
2. 生成應用密碼（名稱可自訂）

**設定應用密碼畫面**

![設定應用密碼](assets/img/set_email_password.png)

3. 設定郵件相關環境變數：
```powershell
# 設定你的 Gmail 帳號
$env:EMAIL_HOST_USER = "your-email@gmail.com"
# 設定應用密碼（16位數，移除空格）
$env:EMAIL_HOST_PASSWORD = "your-app-password"
```

> **重要**: 應用程式密碼是 16 位數密碼，請移除所有空格後再設定到環境變數

### 5. 建立虛擬環境

建立並啟用 Python 虛擬環境：
```bash
# 進入專案目錄
cd email_send_backend

# 建立虛擬環境
python -m venv env

# 啟用虛擬環境
env\Scripts\activate
```

### 6. 安裝相依套件

安裝所需的 Python 套件：
```bash
pip install -r requirements.txt
```


## 資料庫設定

執行資料庫遷移以建立必要的資料表：
```bash
# 生成遷移文件
python manage.py makemigrations

# 執行遷移
python manage.py migrate
```

**資料庫安裝成功畫面**

![安裝資料表](assets/img/install_apps.png)

## 啟動服務

啟動 Django 開發服務器：
```bash
python manage.py runserver 0.0.0.0:8000
```

**服務啟動成功畫面**

![運行資訊](assets/img/server_information.png)

## API 文檔

### 基礎信息
- **Base URL**: `http://localhost:8000/api/`
- **認證方式**: Token Authentication
- **內容類型**: `application/json`

### API 端點

| 端點 | 方法 | 描述 | 認證 |
|------|------|------|------|
| `/api/send_code_email/` | POST | 發送驗證碼到郵箱 | 無 |
| `/api/register/` | POST | 用戶註冊 | 無 |
| `/api/login/` | POST | 用戶登入 | 無 |
| `/api/delete_account/` | POST | 刪除帳號 | 需要 |

#### 1. 發送驗證碼
```http
POST /api/send_code_email/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**回應**:
```json
{
  "message": "驗證碼已發送，請檢查垃圾郵件"
}
```

#### 2. 用戶註冊
```http
POST /api/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "securepassword123",
  "code": "123456"
}
```

**回應**:
```json
{
  "message": "註冊成功"
}
```

#### 3. 用戶登入
```http
POST /api/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**回應**:
```json
{
  "message": "登入成功",
  "username": "testuser",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### 4. 刪除帳號
```http
POST /api/delete_account/
Content-Type: application/json
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**回應**:
```json
{
  "message": "帳號已刪除"
}
```

## 完整測試流程

使用 HOPPSCOTCH 或其他 API 測試工具進行測試：

### 1. 驗證碼發送測試

![測試1](assets/img/test1.png)

![測試2](assets/img/test2.png)

### 2. 用戶註冊測試

![測試3](assets/img/test3.png)

### 3. 用戶登入測試

![測試4](assets/img/test4.png)

### 4. 帳號刪除測試

![測試5](assets/img/test5.png)

![測試6](assets/img/test6.png)

## 注意事項

### 安全性提醒
- 請勿將敏感信息（如密碼、Token）硬編碼在代碼中
- 生產環境請使用更安全的 SECRET_KEY
- 生產環境請關閉 DEBUG 模式
- 請根據需求調整 ALLOWED_HOSTS

### 環境變數檢查清單
確保以下環境變數已正確設定：
- [ ] `DB_PASSWORD` - PostgreSQL 密碼
- [ ] `EMAIL_HOST_USER` - Gmail 帳號
- [ ] `EMAIL_HOST_PASSWORD` - Gmail 應用密碼
- [ ] `SECRET_KEY` - Django 密鑰（生產環境）
