from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/<int:id>', admin.site.urls),
    path('login', views.login),
    path('register', views.regist),
    path('emailverify', views.email_verify),
    path('chkemail', views.check_email),
    path('chkusername', views.check_username),
    path('chkid', views.check_id),
    path('picupload', views.input_pic),
    path('getuserinfo', views.getdata),
    path('changeinfo', views.changeinfo),
    path('logout', views.logout),
    path('shopcar', views.cart),
    path('QQlogin', views.qq_login),
    path('wxlogin', views.wechat_login),
]