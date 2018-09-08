# Create your views here.
from django.http import Http404, JsonResponse, HttpResponse
import json
from .models import Course, Section
from django.db.models import Q
from user.models import User
from django.forms.models import model_to_dict


def needmail(func):
    def inner(*args, **kwargs):  # 1
        req = args[0]
        uid = req.session.get('uid')
        if uid:
            user = User.objects.filter(id__exact=uid)
            user = user[0]
            if not user.emailVerified:
                return HttpResponse(json.dumps({"error": "邮箱未验证！"}))
        return func(*args, **kwargs)  # 2

    return inner


##进入初始界面的时候，根据用户ID和推送算法，加载课程信息
# 根据需求返回课程信息

# 搜索算法搜索课程
def searchCourse(uid, page):
    if uid == -1:
        course = Course.objects.all()  # 选取所有的课程
    else:
        user = User.objects.get(id=uid)
        course = Course.objects.filter(user__id=user.id).select_related()  # 选取uid的所有课程

    course1 = []
    obj_dic = {}
    obj_dic['length'] = (len(course) - 0.5) // 9 + 1
    for o in course:
        # 把Object对象转换成Dict
        dic1 = {}
        dic1['id'] = o.id
        dic1['course_name'] = o.course_name
        dic1['course_info'] = o.course_info
        dic1['course_price'] = o.course_price
        dic1['teacherName'] = o.teacherName
        dic1['picPath'] = o.picPath
        course1.append(dic1)
    len1 = max(9, len(course1))

    obj_dic['data'] = course1[(page - 1) * 9:page * 9]
    return obj_dic


# 搜索小节
#def searchSection(uid, cid):
#    user = User.objects.filter(id=uid)[0]
#    course = Course.objects.filter(id=cid, user__id=user.id).select_related()[0]  # 选取uid的所有课程
#    section = Section.objects.filter(course__id=course.id).select_related()

#    section1 = []
#    obj_dic = {}
#    obj_dic['length'] = len(section)
#    for o in section:
        # 把Object对象转换成Dict
#        dic1 = {}
#        dic1['section_name'] = o.section_name
#        dic1['videoPath'] = o.videoPath
#        section1.append(dic1)

#    # len1 = max(9,len(section1))
#   obj_dic['data'] = section1
#    return obj_dic

    # for o in section:
    # 把Object对象转换成Dict
    # dict = {}
    # dict.update(o.__dict__)
    # dict.pop("_state", None)  # 去除掉多余的字段
    # obj_dic[o.id] = dict
    # obj_dic

    # return obj_dic
    # return model_to_dict(section)
    # columns = [col[0] for col in section.description]
    # return [
    #    dict(zip(columns, row)) for row in section.fetchall()
    # ]


# 返回初始界面课程的信息,类似index，加入界面时返回申请
def getCourseInfo(request, page):
    print(request.COOKIES)
    try:
        data = searchCourse(-1, int(page))  # -1用于表示非用户id，将所有课程推送回来
    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 返回用户购买课程列表，根据uid（所有课程的表）
@needmail
def getCourseInfoUid(request, page):
    print(request.COOKIES)
    try:
        user_id = request.session['uid']
        data = searchCourse(int(user_id), int(page))  # 获取学生id对应的所有课程的所有信息

    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# 返回用户购买课程对应小节的列表，根据uid,cid（对应课程的所有小节表）（暂时没有考虑免费课程获取小节的情况）
#def getSectionInfoUCid(request, course_id):
#    print(request.COOKIES)
#    user_id = request.session['uid']
#    try:
#        data = searchSection(int(user_id), course_id)  # 获取学生id对应的所有课程的所有信息
#    except Section.DoesNotExist:  ##Course 表查找失败
#        raise Http404("课程小节加载失败")
#    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

@needmail
def judgeCourse(request,cid):
    print(request.COOKIES)

    f = False
    try:
        uid = request.session['uid']
        user = User.objects.get(id=int(uid))
        course = Course.objects.filter(id=int(cid), user__id=user.id).select_related()  # 选取uid的所有课程
        f = True
    except Course.DoesNotExist:
        f = False
    except KeyError:
        f = False
        # return JsonResponse({'error': '用户未登录'}, safe=False, json_dumps_params={'ensure_ascii': False})

    dict = {}

    #dic = []
    try:
        course1 = Course.objects.get(id = int(cid))
    except Course.DoesNotExist:
        dict = {'error': '课程不存在'}
        return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

    dic2 = {}
    dic2['id'] = course1.id
    dic2['course_name'] = course1.course_name
    dic2['course_info'] = course1.course_info
    dic2['course_price'] = course1.course_price
    dic2['teacherName'] = course1.teacherName
    dic2['picPath'] = course1.picPath
    #dic.append(model_to_dict(course1))
    dict['course'] = dic2

    print(dict)

    if f:
        if course:
            dict['islearn'] = True
            section = Section.objects.filter(course__id = course1.id).select_related()
            section1 = []
            dict['length'] = len(section)
            for o in section:
                # 把Object对象转换成Dict
                dic1 = {}
                dic1['section_id'] = o.id
                dic1['section_name'] = o.section_name
                dic1['videoPath'] = o.videoPath
                section1.append(dic1)
            dict['section'] = section1
        else:
            dict['islearn'] = False
            #dict['error'] = '课程未购买'
            return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        #dict['islearn'] = False
        dict = {'error': '课程不存在'}
        return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

@needmail
def addCourse(request, cid):
    uid = request.session['uid']
    user = User.objects.get(id=int(uid))
    course = Course.objects.get(id=int(cid))
    course.user.add(user)
    dict = {'Success':'授权成功'}
    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})


def keySearch(request):

    key = request.GET['key']
    if not key:
        dict = {'Error': '未购买此课程！'}
        return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

    obj_dic = {}
    try:
        #查询课程名 | 查询教师
        post_list = Course.objects.filter(Q(course_name__icontains = key) | Q(teacherName__icontains = key) | Q(course_info__icontains = key))
        course1 = []

        obj_dic['length'] = len(post_list) #查找结果个数
        for o in post_list:
            # 把Object对象转换成Dict
            dic1 = {}
            dic1['id'] = o.id
            dic1['course_name'] = o.course_name
            dic1['course_info'] = o.course_info
            dic1['course_price'] = o.course_price
            dic1['teacherName'] = o.teacherName
            dic1['picPath'] = o.picPath
            course1.append(dic1)

        obj_dic['courseinfo'] = course1

    except Course.DoesNotExist:  ##Course 表查找失败
        raise Http404("课程加载失败")
    return JsonResponse(obj_dic, safe=False, json_dumps_params={'ensure_ascii': False})


#获取一条评论,参数为字典类型，包含sid和str
@needmail
def addEvaluation(request):
    uid = request.session['uid']
    sid = request.GET['sid']  #篇id

    try:
        user = User.objects.get(id = int(uid))
    except User.DoesNotExist:
        raise Http404("用户查找失败")
    try:
        section = Section.objects.get(id = int(sid))
    except Section.DoesNotExist:
        raise Http404("视频查找失败")

    dic = {}
    dic['uid'] = uid
    dic['username'] = user.username
    dic['userpic'] = user.picture
    dic['str'] = request.GET['str']

    section.evaluation.append(dic)
    #pian1.length = pian1.length+1
    dict = {'Success': '添加成功'}
    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

#返回一小节对应的所有评论
@needmail
def getEvaluation(request,sid):
    try:
        section = Section.objects.get(id = sid)
    except Section.DoesNotExist:
        raise Http404("此页查找失败")
    dict = {}
    dic = section.evaluation
    dict['length'] = len(dic)
    dict['evaluation'] = dic
    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})