
from django.urls import path
from . import views

urlpatterns = [
    #ex: /course/
    path('all/<int:index>',views.getCourseInfo),
    #ex: /course/user_id/
    path('<int:user_id>/', views.getCourseInfoUid),
    path('<int:uid>/<int:cid>',views.judgeCourse),
    path('<int:user_id>/<int:course_id>', views.getSectionInfoUCid),
]