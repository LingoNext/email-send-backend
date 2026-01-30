
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import random
import requests

@api_view(['POST'])
def send_code_email(request):
    """
        驗證碼 API：向指定的電子郵件發送驗證碼。
    """

    # 產生六位數的驗證碼
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    # 從請求取得 email
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    subject = "專題程式的驗證碼"
    message = f"""您好：

您的驗證碼為：{code}
請於五分鐘內完成註冊。

若您並未進行註冊，請直接忽略此郵件，無需進行任何操作。

英語學習小幫手 APP
國立臺中科技大學 CSIE
2026 資訊與流通學院 大學部畢業專題
開發團隊：LingoNext

網頁版專題展示(使用手機 APP 更佳)：
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
            "text": message,
        }
    )

    if response.status_code == 200:
        return Response({'message': '驗證碼已成功發送。'}, status=status.HTTP_200_OK,content_type='application/json; charset=utf-8')
    else:
        return Response({'error': '郵件發送失敗。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type='application/json; charset=utf-8')