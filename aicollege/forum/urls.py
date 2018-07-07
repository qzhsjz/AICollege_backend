from django.urls import path
from . import views

urlpatterns = [
    path('/', views.test),
    path(r'^addevaluation/(?P<str>\w+)/$',views.addEvaluation),
    path('getevaluation/<int:pid>',views.getEvaluation),
]