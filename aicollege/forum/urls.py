from django.urls import path
from . import views

urlpatterns = [
    path('forum', views.ctrl_forum),
    path('thread', views.ctrl_thread),
]