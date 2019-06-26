"""mywebsite1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from goods import user_view, goods_view, address_view, orders_view
from mywebsite1 import settings

"""
2.0 版本
"""
urlpatterns = [
    path('', user_view.index),
    path('admin/', admin.site.urls),
    path('index/', user_view.index, name='index'),
    path('login_action/', user_view.login_action, name='login_action'),
    path('logout/', user_view.logout, name='logout'),
    path('register/', user_view.register, name='register'),
    path('user_info/', user_view.user_info, name='user_info'),
    path('change_password/', user_view.change_password),
    path('goods_view/', goods_view.goods_view),
    path('search_name/', goods_view.search_name),
    re_path(r'^view_goods/(?P<good_id>[0-9]+)/$', goods_view.good_detail),
    re_path(r'^add_chart/(?P<good_id>[0-9]+)/(?P<sign>[0-9]+)/$', goods_view.add_chart),
    path('view_chart/', goods_view.view_chart),
    re_path(r'^update_chart/(?P<good_id>[0-9]+)/$', goods_view.update_chart),
    re_path(r'^remove_chart/(?P<good_id>[0-9]+)/$', goods_view.remove_chart),
    path('remove_chart_all/', goods_view.remove_chart_all),
    path('view_address/', address_view.view_address),
    re_path(r'^add_address/(?P<sign>[0-9]+)/$', address_view.add_address),
    re_path(r'^update_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$', address_view.update_address),
    re_path(r'^delete_address/(?P<address_id>[0-9]+)/(?P<sign>[0-9]+)/$', address_view.delete_address),
    path('create_order/', orders_view.create_order),
    re_path(r'view_orders/(?P<orders_id>[0-9]+)/$', orders_view.view_orders),
    path('view_all_orders/', orders_view.view_all_orders),
    re_path(r'delete_orders/(?P<orders_id>[0-9]+)/(?P<sign>[0-9]+)/$', orders_view.delete_orders),
]+ static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)+\
    static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)

