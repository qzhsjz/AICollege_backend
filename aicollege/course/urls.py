
from django.urls import path
from . import views

urlpatterns = [
    #ex: /course/
    path('all/<int:page>',views.getCourseInfo),
    #ex: /course/user_id/
    path('mystudy/<int:page>', views.getCourseInfoUid),
    path('<int:cid>',views.judgeCourse),
    #path('<int:course_id>', views.getSectionInfoUCid),
    path('addtostudy/<int:cid>',views.addCourse),
    path(r'^keysearch/(?P<key>\w+)/$',views.keySearch),
    path('addEvaluation/<dict:dic>',views.addEvaluation),
    path('getevaluation/<int:sid>',views.getEvaluation),
]