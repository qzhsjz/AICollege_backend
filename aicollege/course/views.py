# Create your views here.
from django.http import Http404,JsonResponse
from .models import Course

##进入初始界面的时候，根据用户ID和推送算法，加载课程信息
#根据需求返回课程信息


#搜索算法搜索课程
def searchCourse(user_id):
    course = Course.objects.filter(student__id = user_id)
    columns = [col[0] for col in course.description]
    return [
        dict(zip(columns, row)) for row in course.fetchall()
    ]

#返回课程信息
def getCourseInfo(request,user_id):

    try:
        data = searchCourse(user_id)  #获取学生id对应的所有课程的所有信息

    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
