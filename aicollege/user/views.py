from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from .models import User
from django.template import loader

# Create your views here.


class UserForm(forms.Form):
     username = forms.CharField(label='用户名', max_length=50)
     password = forms.CharField(label='密码', widget=forms.PasswordInput())
     email = forms.EmailField(label='邮箱')


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

            if user1|user2:
                return render_to_response('index.html', {'userform': userform})
            else:
                return HttpResponse('用户名邮箱或密码错误,请重新登录')

        else:
            userform = UserForm()
        return render_to_response('login.html', {'userform': userform})


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
        userform = UserForm()
    return render_to_response('login.html',{'userform':userform})


def check_email(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            email = userform.cleaned_data['email']

            user2 = User.objects.filter(email__exact=email)
            if user2:
                return HttpResponse('邮箱已注册')
    else:
        userform = UserForm()
    return render_to_response('login.html',{'userform':userform})