from django.db import models

# Create your models here.


class User(models.Model):
    #用户ID
    # user_id = models.AutoField()
    #用户头像
    #picture = models.CharField(max_length=255)
    #upload_to 会在项目根目录下的media中创建userpic路径，这个文件夹用以保存所有用户头像
    picture = models.ImageField(upload_to='userpic',default='userpic/default.jpg')
    #用户名
    username = models.CharField(max_length=50)
    #密码
    password = models.CharField(max_length=128)
    #用户邮箱
    email = models.EmailField()
    emailVerified = models.BooleanField()
    emailCode = models.CharField(max_length=64)
    #身份验证，是否为老师
    isTeacher = models.BooleanField(default=False)
    #推荐人，通过用户ID来绑定
    referrer = models.IntegerField()

#Teacher,Student 扩展类
class Teacher(User):
    job_title = models.CharField(max_length = 255)

class Student(User):
    admission_time = models.DateTimeField('date published')