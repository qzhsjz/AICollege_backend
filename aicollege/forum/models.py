from django.db import models
from course.models import Course,Section
from user.models import User
# Create your models here.

# class pian:
# #     id = models.AutoField(primary_key=True)
# #     section = models.ForeignKey(Section, on_delete=models.CASCADE)  # 强实体的sid
# #
# #     evaluation = []  #评价数组，每个元素是个字典，字典中包含学生id和学生的评论
# #     size = models.IntegerField(default=0)  #评价的条数


class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    manager = models.ManyToManyField(User)
    picture = models.CharField(max_length=255)
    description = models.TextField()


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_published = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    content = models.TextField()
    related_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    related_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)


class Attachment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=2048)


class DownloadTicket(models.Model):
    id = models.AutoField(primary_key=True)
    target = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    secret = models.CharField(max_length=64)
    ipv4 = models.IPAddressField(protocol="ipv4")
    ipv6 = models.IPAddressField(protocol="ipv6")
    count = models.IntegerField(default=0)
    expired_time = models.DateTimeField()