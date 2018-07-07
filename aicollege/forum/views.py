from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from .models import pian

def test(request):
    return HttpResponse("here.")

#获取一条评论
def addEvaluation(request,str):
    uid = request.session['uid']
    pid = request.session['pid']  #篇id
    dic = {}
    dic['uid'] = uid
    dic['evaluation'] = str
    try:
        pian1 = pian.objects.get(id = pid)
    except pian.DoesNotExist:
        raise Http404("此页查找失败")
    pian1.evaluation.append(dic)
    #pian1.length = pian1.length+1
    dict = {'Success': '添加成功'}
    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})

#返回一页的所有评论
def getEvaluation(request,pid):
    try:
        pian1 = pian.objects.get(id = pid)
    except pian.DoesNotExist:
        raise Http404("此页查找失败")
    dict = {}
    dic = pian1.evaluation
    #length = pian1.length
    dict['length'] = len(dic)
    dict['eva'] = dic
    return JsonResponse(dict, safe=False, json_dumps_params={'ensure_ascii': False})
