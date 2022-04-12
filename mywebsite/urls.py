"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include  # include other app

from django.contrib.auth import views
from company.views import Login

# Add static for image field
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings  # ดึงไฟล์ settings มาใส่ในไฟล์นี้ ให้ใช้ MEDIA ได้

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('company.urls')),  # link project to app
    path('login/', views.LoginView.as_view(template_name='company/login.html'),
         name="login"),  # ตรงนี้คือส่วนที่ดึงหน้า Login มาแสดงผล เฉยๆ ไม่ใช่การส่งฟอร์ม
    path('logout/', views.LogoutView.as_view(template_name='company/logout.html'),
         name="logout"),  # link project to app
    # ตรงนี้คือส่วนที่ดึงหน้า Login มาแสดงผล เฉยๆ ไม่ใช่การส่งฟอร์ม
    path('login/', Login, name="login"),

]

urlpatterns += staticfiles_urlpatterns()
# ทำให้ ระบบรู้ว่า URL ของไฟล์ MEDIA (MEDIA_URL) มี ไฟล์อยู่ที่ MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
