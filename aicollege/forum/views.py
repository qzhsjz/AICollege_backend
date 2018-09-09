from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from .models import *
from user.models import User

def ctrl_forum(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            frmroot = Forum.objects.get(id=int(request.GET['id']))
        else:
            frmroot = None
        child_set = Forum.objects.filter(parent=frmroot).all()
        rtnlst = []
        for child in child_set:
            managers = child.manager.all()
            mlst = []
            for m in managers:
                mlst.append({
                    'uid': m.id,
                    'username': m.username,
                    'picture': m.picture,
                })
            rtnlst.append({
                'id': child.id,
                'name': child.name,
                'picture': child.picture,
                'parent_id': frmroot.id if frmroot else None,
                'manager_list': mlst,
            })
        return JsonResponse(rtnlst, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'POST':
        if request.session.get('uid'):
            uid = request.session.get('uid')
            user = User.objects.get(id=uid)
            if user.isForumAdmin:
                if request.POST.get('id'):
                    try:
                        frm = Forum.objects.get(id=int(request.POST['id']))
                    except Forum.DoesNotExist:
                        return JsonResponse({'error': '不存在编号为' + request.POST['id'] + '的版块'}, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    frm = Forum()
                if request.POST.get('name'):
                    frm.name = request.POST['name']
                if request.POST.get('description'):
                    frm.description = request.POST['description']
                # TODO: 这里需要设计如何更改版主、更改版块图片以及更改上级版块。
            else:
                return JsonResponse({'error': '用户无权限'}, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'error': '用户未登录'}, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'error': '请求不合法'}, safe=False, json_dumps_params={'ensure_ascii': False})

def ctrl_thread(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            t = Thread.objects.get(id=int(request.GET['id']))
        else:
            return JsonResponse({'error': '未指定帖子id'}, safe=False, json_dumps_params={'ensure_ascii': False})
        child_set = Thread.objects.filter(parent=t).all()
        reply_lst = []
        for child in child_set:
            reply_lst.append({
                'id': child.id,
            })
        rtn_obj = {
            'id': t.id,
        }
        return JsonResponse(rtn_obj, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'POST':
        if request.session.get('uid'):
            uid = request.session.get('uid')
            user = User.objects.get(id=uid)
            if request.POST.get('id'):
                t = Thread.objects.get(id=int(request.POST['id']))
            else:
                t = Thread()
            # TODO: 对帖子的各种操作
        else:
            return JsonResponse({'error': '用户未登录'}, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'error': '请求不合法'}, safe=False, json_dumps_params={'ensure_ascii': False})