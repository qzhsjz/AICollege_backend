from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    #用户ID
    # user_id = models.AutoField()
    #用户头像
    #picture = models.CharField(max_length=255)
    #upload_to 会在项目根目录下的media中创建userpic路径，这个文件夹用以保存所有用户头像
    picture = models.CharField(max_length=255)
    #用户名
    username = models.CharField(max_length=50)
    #密码
    password = models.CharField(max_length=128)
    #用户邮箱
    email = models.EmailField()
    emailVerified = models.BooleanField()
    emailCode = models.CharField(max_length=64, default=0)
    #身份验证，是否为老师
    isTeacher = models.BooleanField(default=False)
    #推荐人，通过用户ID来绑定
    referrer = models.IntegerField()
    #推荐人的数量
    countRefer = models.IntegerField(default=0)
    isVIP = models.BooleanField(default=False)

    #关联的QQ
    qq_openid = models.CharField(max_length=64)
    qq_name = models.CharField(max_length=50)
    qq_picture = models.CharField(max_length=255)

    #关联微信
    wx_id = models.CharField(max_length=64)
    wx_name = models.CharField(max_length=50)
    wx_picture = models.CharField(max_length=255)

    # 购物车
    cart = models.TextField()


#Teacher,Student 扩展类
class Teacher(User):
    job_title = models.CharField(max_length = 255)


class Student(User):
    admission_time = models.DateTimeField('date published')


#user表的外键，用于保存用户邀请的人的ID
class InviteUser(models.Model):
    invite_id = models.AutoField(primary_key=True)
    # 邀请人
    user = models.ForeignKey(User,on_delete=models.CASCADE)