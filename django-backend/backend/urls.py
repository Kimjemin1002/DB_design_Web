from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지
    path('api/', include('api.urls')),  # API 앱의 URL 포함
]
