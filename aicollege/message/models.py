from django.db import models
from user.models import User

# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name=sender)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name=receiver)
    time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()