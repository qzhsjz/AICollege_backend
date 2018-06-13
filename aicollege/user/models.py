from django.db import models

# Create your models here.


class User(models.Model):
    #用户ID
    userID = models.IntegerField(max_length=10)
    #用户头像
    picture = models.CharField(max_length=255)
    #用户名
    username = models.CharField(max_length=50)
    #密码
    password = models.CharField(max_length=50)
    #用户邮箱
    email = models.EmailField()
    #身份验证，是否为老师
    isTeacher = models.BooleanField
    #推荐人，通过用户ID来绑定
    referrer = models.IntegerField(max_length=10)