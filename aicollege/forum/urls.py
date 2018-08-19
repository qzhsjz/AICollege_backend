from django.urls import path
from . import views

urlpatterns = [
    path('/', views.test),
    #path('addEvaluation/<dict:dic>',views.addEvaluation),
    #path('getevaluation/<int:sid>',views.getEvaluation),
]