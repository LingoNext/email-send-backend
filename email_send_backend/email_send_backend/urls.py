from django.urls import path
from myapp.views import send_verification_code

urlpatterns = [
    path('api/send_verification_code/', send_verification_code, name='send_code_email'),
]
