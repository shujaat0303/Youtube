from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
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
    subscribers = models.ManyToManyField(User, related_name='subscribed_to', blank=True)
    def is_user_subscribed(self, user):
        return user in self.subscribers.all()
    


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=4000)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="video")
    time = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(upload_to='images/thumbnail',default=None, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            ])
    video = models.FileField(upload_to='videos/',default=None, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv']),
            ])
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    num_views = models.IntegerField(default=0)
    def has_user_liked(self, user):
        return user in self.likes.all()


class Comment(models.Model):
    comment = models.CharField(max_length=4000)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    on = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comment")
    time = models.DateTimeField(auto_now_add=True)
    num_comments = models.IntegerField(default=0)


class WatchHistory(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    on = models.ForeignKey(Video, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)