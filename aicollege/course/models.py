# Create your models here.
from django.db import models
from __future__ import unicode_literals
from aicollege.user.models import Student,Teacher

#强实体集
class Course(models.Model):
    course_id = models.AutoField()
    course_name = models.CharField(max_length=255)
    credit = models.IntegerField(default=4)          #默认4学分
    course_hours = models.IntegerField(default=48)   #默认48学时
    course_info = models.TextField()                 #课程相关信息
    course_price = models.FloatField()                      #费用,一整套课的费用
    course_data = models.DateTimeField('date published')    #课程发布时间
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)    #老师与课程的关系为1对多
    students = models.ManyToManyField(Student)                       #学生与课程的关系是多对多
    pic = models.ImageField(upload_to='')                            #这一块是图片上传过来后储存到数据库中

#弱实体集，课程的小节， 依赖cid
class Section(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)    #强实体的cid
    section_id = models.AutoField()
    section_name = models.CharField(max_length = 255)
    section_info = models.TextField()          #小节对应的课程信息
    section_price = models.FloatField()        #当对应的课程的费用已付，无需支付小节费用
    section_data = models.DateTimeField('date published')
    pic = models.ImageField(upload_to='')