# Create your views here.
from django.http import Http404,JsonResponse
from .models import Course,Section
from user.models import User
from django.forms.models import model_to_dict

##进入初始界面的时候，根据用户ID和推送算法，加载课程信息
#根据需求返回课程信息

#搜索算法搜索课程
def searchCourse(uid,page):
    if uid == -1:
        course = Course.objects.all()  #选取所有的课程
    else:
        user = User.objects.filter(id = uid)[0]
        course = Course.objects.filter(user__id = user.id).select_related()  #选取uid的所有课程

    course1 = []
    obj_dic = {}
    obj_dic['length'] = (len(course)-0.5)// 9+1
    for o in course:
        # 把Object对象转换成Dict
        course1.append(model_to_dict(o))
    len1 = max(9, len(course1))

    obj_dic['data'] = course1[(page-1)*9:min((page-1)*9+8,len1-1)]
    return obj_dic

#搜索小节
def searchSection(uid,cid):
    user = User.objects.filter(id = uid)[0]
    course = Course.objects.filter(id=cid, user__id=user.id).select_related()[0]  # 选取uid的所有课程
    section = Section.objects.filter(course__id = course.id).select_related()

    section1 = []
    obj_dic = {}
    obj_dic['length'] = len(section)
    for o in section:
        # 把Object对象转换成Dict
        section1.append(model_to_dict(o))

    #len1 = max(9,len(section1))
    obj_dic['data'] = section1
    return obj_dic

    #for o in section:
        # 把Object对象转换成Dict
        #dict = {}
        #dict.update(o.__dict__)
        #dict.pop("_state", None)  # 去除掉多余的字段
        #obj_dic[o.id] = dict
        #obj_dic

    #return obj_dic
    #return model_to_dict(section)
    #columns = [col[0] for col in section.description]
    #return [
    #    dict(zip(columns, row)) for row in section.fetchall()
    #]

#返回初始界面课程的信息,类似index，加入界面时返回申请
def getCourseInfo(request,page):
    print(request.session.keys())
    try:
        data = searchCourse(-1,int(page))  #-1用于表示非用户id，将所有课程推送回来
    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

#返回用户购买课程列表，根据uid（所有课程的表）
def getCourseInfoUid(request,page):
    print(request.session.keys())
    user_id = request.session['uid']
    try:
        data = searchCourse(int(user_id),int(page))  #获取学生id对应的所有课程的所有信息

    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


#返回用户购买课程对应小节的列表，根据uid,cid（对应课程的所有小节表）（暂时没有考虑免费课程获取小节的情况）
def getSectionInfoUCid(request,course_id):
    print(request.session.keys())
    user_id = request.session['uid']
    try:
        data = searchSection(int(user_id),course_id)  #获取学生id对应的所有课程的所有信息
    except Section.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程小节加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def judgeCourse(request,cid):
    print(request.session.keys())
    uid = request.session['uid']
    #uid=10
    user = User.objects.filter(id= int(uid))[0]
    course = Course.objects.filter(id=cid, user__id=user.id).select_related()  # 选取uid的所有课程
    dict = {}
    dic = []
    if course:
        dict['islearn'] = True
    else:
        dict['islearn'] = False
    course1 = Course.objects.filter(id=cid)[0]
    dic.append(model_to_dict(course1))
    dict['course'] = dic

    section = Section.objects.filter(course__id=course1.id).select_related()
    section1 = []
    dict['length'] = len(section)
    for o in section:
        # 把Object对象转换成Dict
        section1.append(model_to_dict(o))
    dict['section'] = section1

    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})
