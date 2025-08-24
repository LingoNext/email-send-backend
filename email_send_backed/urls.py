"""
Definition of urls for email_send_backed.
"""

from django.urls import path
from app.views import send_code_email,register,login,delete_account

urlpatterns = [
    path('api/send_code_email/', send_code_email, name='send_code_email'),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/delete_account/', delete_account, name='delete_account')
]