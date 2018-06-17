
from django.urls import path
from . import views

urlpatterns = [
    #ex: /course/
    path('all',views.getCourseInfo),
    #ex: /course/user_id/
    path('', views.getCourseInfoUid),
    path('<int:cid>',views.judgeCourse),
    path('<int:course_id>', views.getSectionInfoUCid),
]