from django.shortcuts import render
from .models import *
from user.models import User
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json


# Create your views here.


def getmsg(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        user = User.objects.get(id__exact=uid)
        ancmts = Announcement.objects.all()
        # ancmt = user.Announcement_set.all()
        msgs = Message.objects.filter(receiver=user).all()
        # msg = user.Message_set.all()
        return HttpResponse(json.dumps({'Announcement': [model_to_dict(ancmt) for ancmt in ancmts], 'Message': [model_to_dict(msg) for msg in msgs]}))
    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))


def sendmsg(request):
    if request.method == 'POST':
        try:
            uid = request.session.get('uid')
            user = User.objects.get(id__exact=uid)
            msg = Message(sender=user)
            recvuid = request.POST['receiver']
            receiver = User.objects.get(id__exact=recvuid)
            msg.receiver = receiver
            msg.subject = request.POST['subject']
            msg.content = request.POST['content']
            msg.save()
            return HttpResponse(json.dumps({"success": "OK"}))
        except KeyError:
            return HttpResponse(json.dumps({"error": "请求不合法！"}))
    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))
