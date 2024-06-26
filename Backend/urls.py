"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from demo1.views import query_all, query_by_count_index, home_page, en_register, ue_reg
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page), # 所有记录
    path('index/', home_page), # 主页
    path('index/<int:count_index>', query_by_count_index), # 所有记录
    path('index/all', query_all), # 指定计数器的记录
    path('all/', query_all), # 指定计数器的记录
    path('EN_Register', en_register), # 小区注册到基站
    # path('UE_Reg', ue_reg) # 手机号注册到基站
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
