from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import secrets
import requests


def get_client_ip(request):
    """
    獲取客戶端真實 IP 地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
def send_verification_code(request):
    """
        驗證碼 API：向指定的電子郵件發送驗證碼。
    """
    email = request.data.get('email')
    purpose = request.data.get('purpose')
    if not email or not purpose:
        return Response({'message': '缺少必要的參數'}, status=status.HTTP_400_BAD_REQUEST)

    # 產生六位數的驗證碼
    code = ''.join(str(secrets.randbelow(10)) for _ in range(6))

    # 取得客戶端資訊
    client_ip = get_client_ip(request)

    # 根據用途設定動作描述和驗證網址
    action_map = {
        'register': '註冊帳戶',
        'reset_password': '重設密碼',
        'login': '登入驗證',
        'change_email': '更換郵箱',
    }
    action = action_map.get(purpose, '身份驗證')
    # 郵件內容
    subject = "驗證碼通知 - 英語學習小幫手"

    # HTML 郵件模板
    html_message = f"""
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>驗證碼通知</title>
  <style>
    body {{
      margin:0; padding:0;
      background:#f9f9f9;
      font-family: Arial, sans-serif;
      color:#111;
    }}
    .container {{
      max-width:500px;
      margin:24px auto;
      background:#fff;
      border-radius:6px;
      padding:20px;
    }}
    .header {{
      text-align:center;
      font-weight:600;
      font-size:18px;
      margin-bottom:16px;
    }}
    .body p {{
      font-size:14px;
      margin:12px 0;
    }}
    .code-card {{
      background:#f4f4f4;
      padding:16px;
      text-align:center;
      border-radius:6px;
      margin:16px 0;
    }}
    .code {{
      font-size:24px;
      letter-spacing:3px;
      font-weight:600;
      color:#0b6efd;
    }}
    .meta {{
      font-size:12px;
      color:#555;
      margin-top:6px;
    }}
    .footer {{
      font-size:12px;
      color:#888;
      text-align:center;
      margin-top:20px;
    }}
    @media (max-width:420px) {{
      .code {{ font-size:20px; }}
      .container {{ padding:14px; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">英語學習小幫手 APP</div>

    <div class="body">
      <p>您好，</p>
      <p>我們收到一筆 <strong>{action}</strong> 的請求。</p>

      <div class="code-card">
        <div class="code">{code}</div>
        <div class="meta">有效期限：5 分鐘</div>
      </div>

      <p style="font-size:12px; color:#555;">
        請求來源 IP：{client_ip}
      </p>

      <p style="font-size:13px; color:#555; margin-top:12px;">
        若您未曾進行此操作，請忽略此郵件。
      </p>
    </div>

    <div class="footer">
      英語學習小幫手 APP 開發團隊 LingoNext<br />
      國立臺中科技大學 資訊工程系 2026 畢業專題
    </div>
  </div>
</body>
</html>
"""

    # 純文字版本作為備用
    text_message = f"""
您好：

您的驗證碼為：{code}
請於五分鐘內完成{action}。

若您並未進行此操作，請直接忽略此郵件，無需進行任何操作。

英語學習小幫手 APP
國立臺中科技大學 資訊工程系
2026 畢業專題
開發團隊：LingoNext

網頁版專題展示：
https://english-learning-assistant.pages.dev/
"""
    # 使用 Resend API 發送郵件
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {getattr(settings, 'SEND_EMAIL_API_KEY', None)}",
            "Content-Type": "application/json"
        },
        json={
            "from": getattr(settings, 'FROM_EMAIL', None),
            "to": [email],
            "subject": subject,
            "html": html_message,
            "text": text_message,
        }
    )

    if response.status_code == 200:
        return Response({'message': '驗證碼已成功發送'}, status=status.HTTP_200_OK,
                        content_type='application/json; charset=utf-8')
    else:
        print(f"郵件發送失敗：{response.status_code} - {response.text}")
        return Response({'message': '郵件發送失敗'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json; charset=utf-8')
