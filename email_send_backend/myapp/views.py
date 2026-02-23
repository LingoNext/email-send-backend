
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

def parse_user_agent(user_agent):
    """
    簡單解析 User-Agent 字符串，提取設備和瀏覽器信息
    """
    if not user_agent or user_agent == 'Unknown':
        return '未知設備'

    # 簡單的設備和瀏覽器檢測
    device = '桌面電腦'
    browser = '未知瀏覽器'

    # 檢測移動設備
    mobile_indicators = ['Mobile', 'Android', 'iPhone', 'iPad', 'iPod']
    for indicator in mobile_indicators:
        if indicator in user_agent:
            if 'iPad' in user_agent:
                device = 'iPad'
            elif 'iPhone' in user_agent or 'iPod' in user_agent:
                device = 'iPhone'
            elif 'Android' in user_agent:
                device = 'Android 設備'
            else:
                device = '移動設備'
            break

    # 檢測瀏覽器
    if 'Chrome' in user_agent and 'Safari' in user_agent:
        if 'Edg' in user_agent:
            browser = 'Microsoft Edge'
        elif 'OPR' in user_agent or 'Opera' in user_agent:
            browser = 'Opera'
        else:
            browser = 'Google Chrome'
    elif 'Firefox' in user_agent:
        browser = 'Mozilla Firefox'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edge' in user_agent:
        browser = 'Microsoft Edge Legacy'

    return f'{device} - {browser}'

@api_view(['POST'])
def send_code_email(request):
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
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    device_info = parse_user_agent(user_agent)

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
    html_message = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>驗證碼通知</title>
  <style>
    /* 基本重置 */
    body {{ margin:0; padding:0; background:#f4f6f8; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", "Helvetica Neue", Arial, sans-serif; color:#111; }}
    .container {{ max-width:600px; margin:24px auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(16,24,40,0.06); }}
    .header {{ background:#0b6efd; color:#fff; padding:16px 20px; display:flex; align-items:center; gap:12px; }}
    .brand {{ font-weight:700; font-size:18px; }}
    .body {{ padding:20px; }}
    .lead {{ font-size:15px; margin-bottom:12px; }}
    .code-card {{ background:#f1f7ff; border:1px solid #e6f0ff; padding:18px; text-align:center; border-radius:8px; margin:12px 0; }}
    .code {{ font-size:28px; letter-spacing:4px; font-weight:700; color:#0b6efd; }}
    .meta {{ color:#6b7280; font-size:13px; margin-top:8px; }}
    .info {{ font-size:13px; color:#374151; margin-top:16px; line-height:1.5; }}
    .footer {{ background:#f8fafc; color:#6b7280; font-size:12px; padding:14px 20px; text-align:center; }}
    @media (max-width:420px) {{
      .code {{ font-size:24px; }}
      .header {{ padding:12px 14px; }}
      .body {{ padding:14px; }}
    }}
  </style>
</head>
<body>
  <div class="container" role="article" aria-label="驗證碼通知">
    <div class="header">
      <div class="brand">英語學習小幫手</div>
      <div style="font-size:13px; opacity:0.9;">LingoNext</div>
    </div>

    <div class="body">
      <p class="lead">您好，</p>

      <p class="lead">我們收到一筆 <strong>{action}</strong> 的請求。</p>

      <div class="code-card" role="region" aria-label="驗證碼">
        <div style="font-size:12px; color:#374151; margin-bottom:6px;">一次性驗證碼</div>
        <div class="code" aria-live="polite">{code}</div>
        <div class="meta">有效期限：<strong>5 分鐘</strong></div>
      </div>


      <div class="info">
        <div><strong>請求來源 IP</strong>：{client_ip}</div>
        <div><strong>裝置資訊</strong>：{device_info}</div>
      </div>

      <p style="margin-top:14px; color:#374151; font-size:13px;">
        若您未曾進行此操作，請忽略此郵件，您的帳戶不會受到影響。
      </p>
    </div>

    <div class="footer">
      英語學習小幫手 APP 開發團隊 LingoNext<br />
      國立臺中科技大學 資訊工程系 2026 畢業專題<br />
      專題展示頁面： https://english-learning-assistant.pages.dev/
    </div>
  </div>
</body>
</html>"""

    # 純文字版本作為備用
    text_message = f"""您好：

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

    from_email = getattr(settings, 'FROM_EMAIL', None)
    api_key = getattr(settings, 'SEND_EMAIL_API_KEY', None)
    recipient_list = [email]

    # 使用 Resend API 發送郵件
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "from": from_email,
            "to": recipient_list,
            "subject": subject,
            "html": html_message,
            "text": text_message,
        }
    )

    if response.status_code == 200:
        return Response({'message': '驗證碼已成功發送'}, status=status.HTTP_200_OK,content_type='application/json; charset=utf-8')
    else:
        print(f"郵件發送失敗：{response.status_code} - {response.text}")
        return Response({'message': '郵件發送失敗'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type='application/json; charset=utf-8')