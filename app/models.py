from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=32)
    birthdate = models.DateField()

    def checkUser(email, password):
        us = User.objects.filter(email=email, password=password)
        if len(us)<1:
            return None
        return us[0]

class Post(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    connected = models.ForeignKey("Post", null=True, on_delete=models.SET_NULL)
    creationdatetime = models.DateTimeField()

class UpVotePost(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)

class TaggedPost(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)

class Chat(models.Model):
    title = models.CharField(max_length=64)

class Message(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()

class UserInChat(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    seen = models.BooleanField(default=False)
