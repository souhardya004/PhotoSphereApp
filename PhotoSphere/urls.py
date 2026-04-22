"""
URL configuration for PhotoSphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('PhotoApp/',include("PhotoApp.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

import shutil
import os
try:
    if not os.path.exists(r'c:\PhotoSphere\static\images\new_login_bg.png'):
        shutil.copy(r'C:\Users\welco\.gemini\antigravity\brain\5de6bc61-1d0b-4b72-b501-f642e5f240e2\new_login_bg_1776884619974.png', r'c:\PhotoSphere\static\images\new_login_bg.png')
    if not os.path.exists(r'c:\PhotoSphere\static\images\new_dashboard_bg.png'):
        shutil.copy(r'C:\Users\welco\.gemini\antigravity\brain\5de6bc61-1d0b-4b72-b501-f642e5f240e2\new_dashboard_bg_1776884633992.png', r'c:\PhotoSphere\static\images\new_dashboard_bg.png')
    if not os.path.exists(r'c:\PhotoSphere\static\images\gallery_bg.png'):
        shutil.copy(r'C:\Users\welco\.gemini\antigravity\brain\5de6bc61-1d0b-4b72-b501-f642e5f240e2\gallery_bg_1776884650436.png', r'c:\PhotoSphere\static\images\gallery_bg.png')
except:
    pass
