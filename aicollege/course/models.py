# Create your models here.
from django.db import models

from aicollege.user.models import Student,Teacher

class Course(models.Model):
    #course_id = models.AutoField()
    course_name = models.CharField(max_length=255)
    credit = models.IntegerField(default=4)          #默认4学分
    course_hours = models.IntegerField(default=48)   #默认48学时
    course_info = models.textField()
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE) #老师与课程的关系为1对多
    students = models.ManyToManyField(Student) #学生与课程的关系是多对多
