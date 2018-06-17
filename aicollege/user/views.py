from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from .models import User
from django.template import loader
import json
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image
from django.forms.models import model_to_dict

# Create your views here.
import random


class UserForm(forms.Form):
     username = forms.CharField(label='用户名', max_length=50)
     password = forms.CharField(label='密码', widget=forms.PasswordInput())
     email = forms.EmailField(label='邮箱')
     id = forms.IntegerField(label='邀请码', max_value=1000000000)   # 邀请码
     enctype = "multipart/form-data"   #头像


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


def login(request):
    if request.method == 'POST':
        print('1')
        #userform = UserForm(request.POST)
        try:
            #nonlocal user
            user = request.POST['username']
            #password = request.POST['password']
        except KeyError:
            return  HttpResponse("用户名不能为空")
        print('2')
        try:
            #nonlocal password
            #user = request.POST['username']
            password = request.POST['password']
        except KeyError:
            return  HttpResponse("密码不能为空")
        print('3')
        user1 = User.objects.filter(username__exact=user, password__exact=password)
        user2 = User.objects.filter(email__exact=user, password__exact=password)
        if user1:
            user1_dic = model_to_dict(user1)
            print('user1\n')
            response = HttpResponse(json.dumps(user1_dic))
            response.set_cookie("username",user1_dic['username'])
            return response
        elif user2:
            user2_dic = model_to_dict(user2)
            printf('user2\n')
            response = HttpResponse(json.dumps(user2_dic))
            response.set_cookie("username",user2_dic['username'])
            return response
        else:
            print('else\n')
            return HttpResponse(json.dumps({'error': '用户名或密码错误！'}))
    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))


def regist(request):
    if request.method == 'POST':
        try:
            #nonlocal username
            username = request.POST['username']
        except KeyError:
            return  HttpResponse("用户名不能为空")
        try:
            #nonlocal password
            password = request.POST['password']
        except KeyError:
            return  HttpResponse("密码不能为空")
        try:
            #nonlocal email
            email = request.POST['email']
        except KeyError:
            return  HttpResponse("邮箱不能为空")
        try:
            #nonlocal rfer
            refer = request.POST['refer_id']
        except KeyError:
            return  HttpResponse("邮箱不能为空")

            user1 = User.objects.filter(username__exact=username)
            user2 = User.objects.filter(email__exact=email)
            if user1:
                return HttpResponse('用户名已存在')
            if user2:
                return HttpResponse('邮箱已注册')

            # settings.COUNT=settings.COUNT+1   #f分配userID
            # code = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-', k=64) # 生成邮件验证码-PY3.6
            code = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-') for i in range(0, 64)]
            code = ''.join(code)
            newuser = User(username=username,password=password,email=email,emailVerified=False,emailCode=code,referrer=refer)
            newuser.save()


            mailbody = "欢迎注册小智课堂！请点击以下链接注册：http://api.aicollege.net/user/emailverify?code=" + code + '&username=' + username
            send_mail(subject='注册确认',message=mailbody,from_email='aicollege@126.com',recipient_list=[email],fail_silently=True)

            return HttpResponse('注册成功！')
    else:
        return HttpResponse("请求不合法")

def email_verify(request):
    # try:
    #     print(request.GET)
        code = request.GET['code']
        username = request.GET['username']
        user = User.objects.filter(emailCode=code)
        if user:
            if user[0].username == username:
                user[0].emailVerified = True
                user[0].save()
                return HttpResponse('验证成功！')
        else:
            return HttpResponse('验证失败')
    # except:
    #     return HttpResponse('请求不合法')


#检查username
def check_username(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']

            user1 = User.objects.filter(username__exact=username)
            if user1:
                return HttpResponse('用户名已存在')
    else:
        return HttpResponse('请求不合法')


#检查注册邮箱
def check_email(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']

            user2 = User.objects.filter(email__exact=email)
            if user2:
                return HttpResponse('邮箱已注册')
    else:
        return HttpResponse('请求不合法')


#检查邀请人的userID信息
def check_id(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            id = userform.cleaned_data['邀请码']

            user = User.objects.filter(userid__exact=id)
            if user:
                return json.dumps(user)
            else:
                return HttpResponse('查无此人')
    else:
        return HttpResponse('请求不合法')


def input_pic(request):
    if(request.method == 'POST'):
        inputpic = request.FILES['input_pic']
        #userform = UserForm(request.POST)
        if inputpic:
            img = Image.open(inputpic)
            picturename = 'media/userpic'+request.username
            img.save('media/userpic'+request.username)
            flag = User.objects.filter(username=request.username).update(picture=picturename)

            if flag:
                return HttpResponse('上传成功')
            else:
                return HttpResponse('上传失败')
    else:
        return HttpResponse('请求不合法')
