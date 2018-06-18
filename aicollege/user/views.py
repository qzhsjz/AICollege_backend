from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from .models import User
from django.template import loader
import json
from django.core.mail import send_mail as osdmail
from django.conf import settings
from PIL import Image
from django.forms.models import model_to_dict
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
import threading

# Create your views here.
import random


class UserForm(forms.Form):
     username = forms.CharField(label='用户名', max_length=50)
     password = forms.CharField(label='密码', widget=forms.PasswordInput())
     email = forms.EmailField(label='邮箱')
     id = forms.IntegerField(label='邀请码', max_value=1000000000)   # 邀请码
     enctype = "multipart/form-data"   #头像

class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


def login(request):
    print(request.COOKIES)
    if request.method == 'GET':
        #userform = UserForm(request.POST)
        try:
            #nonlocal user
            user = request.GET['username']
            #password = request.POST['password']
        except KeyError:
            return  HttpResponse("用户名不能为空")

        try:
            #nonlocal password
            #user = request.POST['username']
            password = request.GET['password']
        except KeyError:
            return  HttpResponse("密码不能为空")

        user1 = User.objects.filter(username__exact=user, password__exact=password)
        user2 = User.objects.filter(email__exact=user, password__exact=password)
        if user1:
            user1_dic = model_to_dict(user1[0])
            response = HttpResponse(json.dumps(user1_dic))
            # response.set_cookie("id", user1_dic['id'])
            request.session['uid'] = user1_dic['id']
            return response
        elif user2:
            user2_dic = model_to_dict(user2[0])
            response = HttpResponse(json.dumps(user2_dic))
            # response.set_cookie("id", user2_dic['id'])
            request.session['uid'] = user2_dic['id']
            return response
        else:
            return HttpResponse(json.dumps({'error': '用户名或密码错误！'}))
    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))


def regist(request):
    if request.method == 'POST':
        try:
            #nonlocal username
            username = request.POST['username']
        except KeyError:
            return  HttpResponse(json.dumps({'error': '用户名不能为空！'}))
        try:
            #nonlocal password
            password = request.POST['password']
        except KeyError:
            return  HttpResponse(json.dumps({'error': '密码不能为空！'}))
        try:
            #nonlocal email
            email = request.POST['email']
            try:
                validate_email(email)
            except ValidationError:
                return HttpResponse(json.dumps({'error':'邮箱格式不正确'}))
        except KeyError:
            return  HttpResponse(json.dumps({'error': '邮箱不能为空！'}))
        try:
            #nonlocal rfer
            refer = request.POST['refer_id']
            user = User.objects.filter(id__exact=refer)
            if user:
                pass
            else:
                return HttpResponse(json.dumps({'error': '查无此人！'}))
        except KeyError:
            pass

        user1 = User.objects.filter(username__exact=username)
        user2 = User.objects.filter(email__exact=email)
        if user1:
            return HttpResponse(json.dumps({'error': '用户名已存在！'}))
        if user2:
            return HttpResponse(json.dumps({'error': '邮箱已注册！'}))

        # settings.COUNT=settings.COUNT+1   #f分配userID
        # code = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-', k=64) # 生成邮件验证码-PY3.6
        code = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-') for i in range(0, 64)]
        code = ''.join(code)
        newuser = User(username=username,password=password,email=email,emailVerified=False,emailCode=code,referrer=refer)
        newuser.save()


        hostname = '39.106.19.27:8080'
        verifyurl = "http://" + hostname + "/user/emailverify?code=" + code + '&username=' + username
        mailbody = "欢迎注册小智课堂！请<a href=" + verifyurl + " target=_blank>点击这里</a>验证邮箱，或手动复制以下链接链接注册：<br>" + verifyurl
        # a = send_mail(subject='小智课堂注册确认', body='', html=mailbody, from_email='aicollege@126.com', recipient_list=[email])
        a = osdmail(subject='小智课堂注册确认', message='', html_message=mailbody, from_email='aicollege@126.com', recipient_list=[email])
        print(a)
        print(mailbody)

        return HttpResponse(json.dumps({'success': '注册成功！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))

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
                # return HttpResponse(json.dumps({'success': '验证成功！'}))
                return HttpResponse("""验证成功！欢迎使用小智课堂。""")
        else:
            # return HttpResponse(json.dumps({'error': '验证失败！'}))
            return HttpResponse("""验证失败！请确保你复制的链接正确，或你收到的链接有效。""")
    # except:
    #     return HttpResponse('请求不合法')


#检查username
def check_username(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
        except KeyError:
            return  HttpResponse(json.dumps({'error': '用户名不能为空！'}))

        user1 = User.objects.filter(username__exact=username)
        if user1:
            return HttpResponse(json.dumps({'error': '用户名已存在！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))


#检查注册邮箱
def check_email(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']

            user2 = User.objects.filter(email__exact=email)
            if user2:
                return HttpResponse(json.dumps({'error': '邮箱已注册！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))


#检查邀请人的userID信息
def check_id(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            id = userform.cleaned_data['邀请码']

            user = User.objects.filter(id__exact=id)
            if user:
                return json.dumps(user)
            else:
                return HttpResponse(json.dumps({'error': '查无此人！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))

#上传头像
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


#修改信息
def changeinfo(request):
    if(request.method == 'POST'):
        try:
            name = request.POST['username']
        except KeyError:
            return HttpResponse(json.dumps({'error': '没有username！'}))
        try:
            userimg = request.POST['userimg']
        except KeyError:
            return HttpResponse(json.dumps({'error': '没有userimg！'}))
        try:
            email = request.POST['email']
        except KeyError:
            return HttpResponse(json.dumps({'error': '没有email！'}))

        uid = request.session['uid']
        user = User.objects.filter(id__exact=uid)
        user = user[0]
        if user:
            # 保存头像
            data = request.FILES['imageFile']
            img = Image.open(data)
            adress = '/usr/share/nginx/AICollege_frontend/img/'+user.username+'.jpg'
            img.save(adress)
            print('头像保存成功')
            user.username = name
            user.picture = adress
            user.email = email
            user.save()
            return HttpResponse(json.dumps({'success': '修改成功！'}))
        else:
            return HttpResponse(json.dumps({'error': '无此用户，无法修改！'}))

    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))



#根据session返回数据
def getdata(request):
    try:
        if(request.method == 'GET'):
            print(request.COOKIES)
            uid = request.session['uid']
            user = User.objects.filter(id__exact=uid)
            user = user[0]
            if user:
                user_dic = model_to_dict(user)
                response = HttpResponse(json.dumps(user_dic))
                return response
            else:
                return HttpResponse(json.dumps({'error': '无此用户！'}))
        else:
            return HttpResponse(json.dumps({'error': '请求不合法！'}))
    except KeyError:
        return HttpResponse(json.dumps({'message': 'Session出错（禁用Cookie）或新用户'}))
