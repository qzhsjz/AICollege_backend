
from django.urls import path
from . import views

urlpatterns = [
    #ex: /course/
    path('',views.getCourseInfo),
    #ex: /course/user_id/
    path('<int:user_id>/', views.getCourseInfoUid),

    path('<int:user_id>/<int:course_id>', views.getSectionInfoUCid),
]