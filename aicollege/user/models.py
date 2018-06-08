from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField()
    username = models.CharField(max_length=50)

    password = models.CharField(max_length=50)
    email = models.EmailField()
    authority = models.BooleanField(default=False) #标准用户是否为具有管理权限

#Teacher,Student 扩展类
class Teacher(User):
    job_title = models.CharField(max_length = 255)

class Student(User):
    admission_time = models.DateTimeField('date published')