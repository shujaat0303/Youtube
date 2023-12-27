from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    profile_pic=models.FileField(upload_to='images/pp',default=None, blank=True, null=True)
    pass


class Channel(models.Model):
    by = models.OneToOneField(User, on_delete=models.CASCADE, related_name="channel", blank="True")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length = 4000)
    cover = models.FileField(upload_to='images/cover',default=None, blank=True, null=True)


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="video",)
    date = models.DateTimeField(auto_now_add=True)
    #TODO: Add media settings 
    thumbnail = models.FileField(upload_to='images/thumbnail',default=None, blank=True, null=True)
    video = models.FileField(upload_to='videos/',default=None, blank=True, null=True)


class Comment(models.Model):
    comment = models.CharField(max_length=4000)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    on = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comment")
    time = models.DateTimeField(auto_now_add=True)


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribed_to")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
