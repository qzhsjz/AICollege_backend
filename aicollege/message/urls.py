from django.urls import path
from . import views

urlpatterns = [
    path('getmsg', views.getmsg),
    path('sendmsg', views.sendmsg),
]