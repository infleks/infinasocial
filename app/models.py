from django.db import models
from infinasocial.settings import BASE_DIR
import os


class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=32)
    birthdate = models.DateField()
    photo = models.ImageField(null=True, blank=True,
                              upload_to="static/uploads/user")

    def checkUser(email, password):
        us = User.objects.filter(email=email, password=password)
        if len(us) < 1:
            return None
        return us[0]


class Post(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    connected = models.ForeignKey(
        "Post", null=True, blank=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)
    creationdatetime = models.DateTimeField()
    activitydatetime = models.DateTimeField(null=True, blank=True)
    posttype = models.IntegerField()  # 1 normal, 2 activity, 3 business

    def getNotificationData(user):
        return UpVotePost.objects.raw("select au.id, au.post_id, au.user_id from app_upvotepost au inner join app_post ap on ap.id = au.post_id where ap.user_id=%d and au.seen = 0" % (user.pk) )

class UpVotePost(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)

    def getNotificationData(user):
        return UpVotePost.objects.raw("select au.id, au.post_id, au.user_id from app_upvotepost au inner join app_post ap on ap.id = au.post_id where ap.user_id=%d and au.seen = 0" % (user.pk) )


class TaggedPost(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)


class Chat(models.Model):
    title = models.CharField(max_length=64)
    creationdatetime = models.DateTimeField()


class Message(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    creationdatetime = models.DateTimeField()


class UserInChat(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)
