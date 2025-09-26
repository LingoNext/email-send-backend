"""
URL configuration for email_send_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from myapp.views import send_code_email,register,login,delete_account

urlpatterns = [
    path('api/send_code_email/', send_code_email, name='send_code_email'),
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/delete_account/', delete_account, name='delete_account')
]
