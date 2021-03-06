# Create your models here.
from __future__ import unicode_literals
from django.db import models
from user.models import User,Student,Teacher


# 强实体集
class Course(models.Model):
    id =models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    credit = models.IntegerField(default=4)          # 默认4学分
    course_hours = models.IntegerField(default=48)   # 默认48学时
    course_info = models.TextField()                 # 课程相关信息
    course_price = models.IntegerField()                      # 费用,一整套课的费用
    course_data = models.DateTimeField('date published')    # 课程发布时间
    user = models.ManyToManyField(User)
    teacherName = models.CharField(max_length=255,default='')                    # 讲课老师
    # teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)    # 老师与课程的关系为1对多
    # students = models.ManyToManyField(Student)                       # 学生与课程的关系是多对多
    # pic = models.ImageField(upload_to='')                            # 这一块是图片上传过来后储存到数据库中
    picPath = models.CharField(max_length=255)  # 图片的路径


# 弱实体集，课程的小节， 依赖cid
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)    # 强实体的cid
    section_name = models.CharField(max_length = 255)
    section_info = models.TextField()          # 小节对应的课程信息
    section_data = models.DateTimeField('date published')
    # evaluation = []  # 评价数组，每个元素是个字典，字典中包含学生id和学生的评论
    # pic = models.ImageField(upload_to='')
    picPath = models.CharField(max_length=255)  # 图片的路径
    videoPath = models.CharField(max_length=255)   # 视频的存储路径


class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 在用户被人间蒸发的时候，一定要区分出来并写上==数据删除==
    reply = models.ForeignKey('self', on_delete=models.SET(-1), null=True)  # 在原评论被删除的情况下，需要显示原评论已经删除。
    content = models.TextField()