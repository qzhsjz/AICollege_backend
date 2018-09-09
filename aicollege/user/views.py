from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from .models import User
from message.models import Message
from .models import InviteUser
from django.template import loader
import json
from django.core.mail import send_mail as osdmail
from django.conf import settings
from PIL import Image
from django.forms.models import model_to_dict
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.forms.models import model_to_dict
import threading
from urllib import request,parse
import urllib
from django.utils.http import urlquote
from hashlib import sha1
import hmac
import base64

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

@needmail
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
            refer = int(refer)
            user = User.objects.filter(id__exact=refer)
            if user:
                user.countRefer=user.countRefer+1
                if user.countRefer>=5:
                    user.isVIP = True
                    user.save()
                    #发消息提醒用户
                    message = Message(sender=0, receiver=user, subject="升级会员通知" ,content="恭喜！您已经成为了小智学院的会员，畅享学院付费课程的免费观看特权！快去学习吧！")
                    message.save()
                #pass
            else:
                return HttpResponse(json.dumps({'error': '查无此人！'}))
        except KeyError:
            pass
        except ValueError:
            pass

        user1 = User.objects.filter(username__exact=username)
        user2 = User.objects.filter(email__exact=email)
        if user1:
            return HttpResponse(json.dumps({'error': '用户名已存在！'}))
        if user2:
            return HttpResponse(json.dumps({'error': '邮箱已注册！'}))

        # settings.COUNT=settings.COUNT+1   #f分配userID
        # code = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-', k=64) # 生成邮件验证码-PY3.6
        code = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789--------____') for i in range(0, 64)]
        code = ''.join(code)
        if not refer:
            refer = 0
        newuser = User(username=username,password=password,email=email,emailVerified=False,emailCode=code,referrer=refer, picture='/img/1.jpg')
        newuser.save()


        hostname = '39.106.19.27:8080'
        verifyurl = "http://" + hostname + "/user/emailverify?code=" + code + '&username=' + username
        mailbody = "欢迎注册小智课堂！请<a href=" + verifyurl + " target=_blank>点击这里</a>验证邮箱，或手动复制以下链接链接注册：<br>" + verifyurl
        # a = send_mail(subject='小智课堂注册确认', body='', html=mailbody, from_email='aicollege@126.com', recipient_list=[email])
        a = osdmail(subject='小智课堂注册确认', message='', html_message=mailbody, from_email='aicollege@126.com', recipient_list=[email])
        print(a)
        print(mailbody)

        # #更新InviteUser表
        # newinviteuser = InviteUser(inviteid=newuser.id,user=refer)
        # newinviteuser.save()

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
        try:
            email = request.POST['email']
        except KeyError:
            return  HttpResponse(json.dumps({'error': '邮箱不能为空！'}))
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse(json.dumps({'error': '邮箱格式语法错误！'}))
        user2 = User.objects.filter(email__exact=email)
        if user2:
            return HttpResponse(json.dumps({'error': '邮箱已注册！'}))
        else:
            return HttpResponse(json.dumps({'true': '邮箱可以注册！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))


#检查邀请人的userID信息
def check_id(request):
    if request.method == 'POST':
        id = request.POST['invite_id']
        user = User.objects.filter(id__exact=id)
        if user:
            return json.dumps(user)
        else:
            return HttpResponse(json.dumps({'error': '查无此人！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))

#上传头像
@needmail
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
@needmail
def changeinfo(request):
    if(request.method == 'POST'):
        #try:
         #   name = request.POST['username']
        #except KeyError:
         #   return HttpResponse(json.dumps({'error': '没有username！'}))
        #try:
         #   userimg = request.POST['userimg']
        #except KeyError:
        #    return HttpResponse(json.dumps({'error': '没有userimg！'}))
        #try:
         #   email = request.POST['email']
        #except KeyError:
         #   return HttpResponse(json.dumps({'error': '没有email！'}))

        uid = request.session['uid']
        user = User.objects.filter(id__exact=uid)
        user = user[0]
        if user:
            # 保存头像
            data = request.FILES['file']
            img = Image.open(data)
            webdir = '/usr/share/nginx/AICollege_frontend'
            adress = '/img/avatar/' + str(user.id) + '.jpg'
            img.save(webdir + adress)
            print('头像保存成功')
            #user.username = name
            user.picture = adress
            #user.email = email
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
            #print(request.COOKIES)
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


# 根据sessio传来的ID来查询该用户所推荐的人
@needmail
def getInviteId(request):
    try:
        if(request.method == 'GET'):
            uid = request.session['uid']
            #user = InviteUser.objects.filter(user__exact=uid)
            users = User.objects.filter(referrer__exact=uid).all()
            if len(users) == 0:
                return HttpResponse(json.dumps({'error': '该用户没有推荐其他用户！'}))
            else:
                data = {}
                # user = InviteUser.objects.value()
                lst = []
                for user in users:
                    user = model_to_dict(user)
                    lst.append(user)
                data['list'] = lst
                return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps({'error': '请求不合法！'}))
    except KeyError:
        return HttpResponse(json.dumps({'message': 'Session出错（禁用Cookie）或新用户'}))


#找回密码
def findpassword(request):
    if(request.method == 'GET'):
        uid = request.session['uid']
        user = User.objects.filter(id__exact=uid)
        user = user[0]
        if user:
            password = user.password
            email = user.email
            name = user.username
            hostname = '39.106.19.27:8080'
            #verifyurl = "http://" + hostname + "/user/emailverify?code=" + code + '&username=' + username
            mailbody = "您好，"+name+"!<br>你的密码是 ："+password+"<br>如果不是本人操作，请忽略此邮件"
            # a = send_mail(subject='小智课堂注册确认', body='', html=mailbody, from_email='aicollege@126.com', recipient_list=[email])
            a = osdmail(subject='小智课堂找回密码', message='', html_message=mailbody, from_email='aicollege@126.com',
                    recipient_list=[email])
            return HttpResponse(json.dumps({'true': '找回密码邮件发送成功！'}))
        else:
            return HttpResponse(json.dumps({'error': '无此用户！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))


#退出登录
def logout(request):
    if(request.method == 'GET'):
        del request.session['uid']
        return HttpResponse(json.dumps({'success': '注销成功！'}))
    else:
        return HttpResponse(json.dumps({'error': '请求不合法！'}))

#APPID: 1105892740
#APPKEY: jW6r4KlTkkIJ5Vbe
#QQ第三方登录
def qq_login(request):
    if request.method == 'GET':
        try:
            qq_id = request.GET['openid']
        except KeyError:
            return  HttpResponse(json.dumps({"error": "QQ:openid不能为空"}))

        try:
            qq_key = request.GET['openkey']
        except KeyError:
            return  HttpResponse(json.dumps({"error": "QQ:openkey不能为空"}))

        try:
            pf = request.GET['pf']
        except KeyError:
            return  HttpResponse(json.dumps({"error": "QQ:pf不能为空"}))

        url = r'http://openapi.sparta.html5.qq.com/v3/user/get_info'
        uri = r'/v3/user/get_info'
        #处理appkey.....
        ecurl = urlquote('/v3/user/get_info')
        key = 'appid=1105892740&format=json&openid='+qq_id+'&openkey='+qq_key+'&pf='+pf
        eckey = urlquote(key)

        s_string = 'GET&'+ecurl+'&'+eckey
        appkey = 'jW6r4KlTkkIJ5Vbe&'
        sign = hmac.new(appkey, s_string, sha1).digest()
        sig = base64.b64encode(sign)

        #对各个参数进行URL编码
        ec_openid = urlquote(qq_id+'&')
        ec_openkey = urlquote(qq_key+'&')
        appid = urlquote('1105892740'+'&')
        ec_pf = urlquote(pf+'&')
        ec_sig = urlquote(sig+'&')
        ec_format = urlquote('json&')

        data = {
            'openid': ec_openid,
            'openkey': ec_openkey,
            'appid': appid,
            'sig': ec_sig,
            'pf': ec_pf,
            'format': ec_format
        }
        data = parse.urlencode(data).encode('utf-8')
        req = request.urlopen(url,data)
        page = req.read()
        result = json.load(page)

        user1 = User.objects.filter(qq_openid__exact=qq_id)
        if user1:
            user1_dic = model_to_dict(user1[0])
            response = HttpResponse(json.dumps(user1_dic))
            # response.set_cookie("id", user1_dic['id'])
            request.session['uid'] = user1_dic['id']
            return response
        else:
            if result[0]:
                qq_name = result[3]
                qq_picture = result[8]

                newuser = User(qq_name=qq_name, emailVerified=False, referrer=0, qq_picture=qq_picture)
                newuser.save()
                request.session['uid'] = newuser.id
                request.session['qq_name'] = qq_name
                user1_dic = model_to_dict(newuser)
                response = HttpResponse(json.dumps(user1_dic))
                return response
            else:
                return HttpResponse(json.dumps({"error": "请求用户信息返回码错误"}))

    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))


#微信登录
def wechat_login(request):
    if request.method == 'GET':
        try:
            code = request.GET['code']
        except KeyError:
            return  HttpResponse(json.dumps({"error": "微信code出错"}))

        try:
            state = request.GET['state']
        except KeyError:
            return  HttpResponse(json.dumps({"error": "微信state出错"}))

        url = r'https://api.weixin.qq.com/sns/oauth2/access_token'
        wx_id = 000
        secret = 111
        data = {
            'appid' : wx_id,
            'secret' : secret,
            'code' : code,
            'grant_type' : 'authorization_code'
        }

        data = parse.urlencode(data).encode('utf-8')
        req = request.urlopen(url, data)
        page = req.read()
        result = json.load(page)

        openid = result["openid"]
        access_token = result["access_token"]

        user1 = User.objects.filter(wx_id__exact=wx_id)
        if user1:
            user1_dic = model_to_dict(user1[0])
            response = HttpResponse(json.dumps(user1_dic))
            # response.set_cookie("id", user1_dic['id'])
            request.session['uid'] = user1_dic['id']
            return response
        else:
            #接下来要调出用户信息了！！！
            url = r'https://api.weixin.qq.com/sns/userinfo'
            para = {
                'access_token': access_token,
                'openid' : openid
            }
            para = parse.urlencode(para).encode('utf-8')
            req = request.urlopen(url, para)
            page = req.read()
            res = json.load(page)

            #注意,这里有个坑,res['nickname']表面上是unicode编码,但是里面的串却是str的编码,
            # 举个例子,res['nickname']的返回值可能是这种形式u'\xe9\x97\xab\xe5\xb0\x8f\xe8\x83\x96',
            # 直接存到数据库会是乱码.必须要转成unicode的编码
            wx_name = res["nickname"].encode('iso8859-1').decode('utf-8')
            wx_picture = res["headimgurl"]

            newuser = User(wx_name=wx_name,emailVerified=False, referrer=0, wx_picture=wx_picture)
            newuser.save()
            request.session['uid'] = newuser.id
            request.session['wx_name'] = wx_name
            user1_dic = model_to_dict(newuser)
            response = HttpResponse(json.dumps(user1_dic))
            return response
    else:
        return HttpResponse(json.dumps({"error": "请求不合法！"}))


def cart(request):
    print(request.COOKIES)
    print(request.session.get('uid'))
    if request.session.get('uid') is None:
        return HttpResponse(json.dumps({"error": "请登录！"}))
    else:
        if request.method == 'GET':
            user = User.objects.filter(id__exact=request.session['uid'])
            user = user[0]
            response = HttpResponse(user.cart)
            return response
        elif request.method == 'POST':
            user = User.objects.filter(id__exact=request.session['uid'])
            user = user[0]
            user.cart = request.body.decode('utf-8')
            user.save()
            return HttpResponse(json.dumps({"success": "OK"}))
        else:
            return HttpResponse(json.dumps({"error": "请求不合法！"}))
