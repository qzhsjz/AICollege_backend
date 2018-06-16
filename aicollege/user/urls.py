from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/<int:id>', admin.site.urls),
    path('login/', views.login)
]