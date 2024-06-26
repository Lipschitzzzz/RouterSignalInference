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
from demo1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page), # 所有记录
    path('test/location/<int:ue_id>', query_info_by_ue_id), # 指定ueid的记录
    path('test/location/all', query_info_all), # 所有记录
    path('test/location/add', add_one_location_info), # 指定计数器的记录
    path('test/enci/register', en_register), # 小区注册到基站
    path('test/ue/register', ue_reg) # 手机号注册到基站
]
