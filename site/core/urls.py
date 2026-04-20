"""
URL configuration for core project.

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

from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from main.views import index, load_page, download_file, get_last_image

urlpatterns = [
    path('', index, name='index'),
    path('download/<str:filename>/', download_file, name='download'),
    path('api/<str:page_name>/', load_page, name='load_page'),
    path('api/last-image/', get_last_image, name='last-image'),  # ЭТА СТРОКА КЛЮЧЕВАЯ
    re_path(r'^downloads/(?P<path>.*)$', serve, {
        'document_root': str(settings.BASE_DIR / 'downloads'),
        'show_indexes': True
    }),
]

# Добавьте отладочный вывод
print("DEBUG: urlpatterns loaded")
for pattern in urlpatterns:
    print(f"  {pattern}")
