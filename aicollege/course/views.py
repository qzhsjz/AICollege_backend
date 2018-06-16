# Create your views here.
from django.http import Http404,JsonResponse
from .models import Course,Section
from aicollege.user.models import User

##进入初始界面的时候，根据用户ID和推送算法，加载课程信息
#根据需求返回课程信息

#搜索算法搜索课程
def searchCourse(uid):
    if uid == -1:
        course = Course.bbjects.all()  #选取所有的课程
    else:
        user = User.objects.filter(user_id = uid)
        course = Course.objects.filter(user_id = user.user_id).select_related()  #选取uid的所有课程

    columns = [col[0] for col in course.description]
    return [
        dict(zip(columns, row)) for row in course.fetchall()
    ]

#搜索小节
def searchSection(uid,cid):
    user = User.objects.filter(user_id = uid)
    course = Course.objects.filter(course_id=cid, user__user_id=user.user_id).select_related()  # 选取uid的所有课程
    section = Section.objects.filter(course_id = course.course_id).select_related()

    columns = [col[0] for col in section.description]
    return [
        dict(zip(columns, row)) for row in section.fetchall()
    ]

#返回初始界面课程的信息,类似index，加入界面时返回申请
def getCourseInfo(request):
    try:
        data = searchCourse(-1)  #-1用于表示非用户id，将所有课程推送回来
    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


#返回用户购买课程列表，根据uid（所有课程的表）
def getCourseInfoUid(request,user_id):
    try:
        data = searchCourse(user_id)  #获取学生id对应的所有课程的所有信息
    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


#返回用户购买课程对应小节的列表，根据uid,cid（对应课程的所有小节表）（暂时没有考虑免费课程获取小节的情况）
def getSectionInfoUCid(request,user_id,course_id):
    try:
        data = searchSection(user_id,course_id)  #获取学生id对应的所有课程的所有信息
    except Section.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程小节加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})