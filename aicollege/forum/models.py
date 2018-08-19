from django.db import models
from course.models import Course,Section
# Create your models here.

class pian:
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)  # 强实体的sid

    evaluation = []  #评价数组，每个元素是个字典，字典中包含学生id和学生的评论
    size = models.IntegerField(default=0)  #评价的条数