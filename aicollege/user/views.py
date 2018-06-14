from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from .models import User
from django.template import loader
import json

# Create your views here.


class UserForm(forms.Form):
     username = forms.CharField(label='用户名', max_length=50)
     password = forms.CharField(label='密码', widget=forms.PasswordInput())
     email = forms.EmailField(label='邮箱')
     id = forms.IntegerField(label='邀请码', max_value=1000000000)   #邀请码


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            user = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user1 = User.objects.filter(username__exact=user, password__exact=password)
            user2 = User.objects.filter(email__exact=user, password__exact=password)

            if user1:
                return json.dumps(user1)
            if user2:
                return json.dumps(user2)
            else:
                return HttpResponse('用户名邮箱或密码错误,请重新登录')
        else:
            userform = UserForm()
        return HttpResponse('不能为空')


def regist(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            user1 = User.objects.filter(username__exact=username)
            user2 = User.objects.filter(email__exact=email)
            if user1:
                return HttpResponse('用户名已存在')
            if user2:
                return HttpResponse('邮箱已注册')

            User.objects.create(username=username,password=password,email=email)
            User.save()

            return HttpResponse('注册成功！')
    else:
        userform = UserForm()
    return render_to_response('login.html',{'userform':userform})


def check_username(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']

            user1 = User.objects.filter(username__exact=username)
            if user1:
                return HttpResponse('用户名已存在')
    else:
        return HttpResponse('用户名不能为空')


def check_email(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']

            user2 = User.objects.filter(email__exact=email)
            if user2:
                return HttpResponse('邮箱已注册')
    else:
        return HttpResponse('邮箱不能为空')


def check_id(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            id = userform.cleaned_data['邀请码']

            user = User.objects.filter(userid__exact=id)
            if user:
                return json.dumps(user)
            else:
                return HttpResponse('没有此人')