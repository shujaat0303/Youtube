from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass

class Channel(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="channel")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=4000)
    # cover


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="video")
    date = models.DateTimeField(auto_now_add=True)
    # thumbnail
    # video



class Comment(models.Model):
    comment = models.CharField(max_length=4000)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    on = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comment")
    time = models.DateTimeField(auto_now_add=True)
