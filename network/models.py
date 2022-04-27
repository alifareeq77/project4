from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Following(models.Model):
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)


class Post(models.Model):
    post = models.CharField(max_length=15000)
    user = models.ForeignKey(User, related_name='post_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class Follower(models.Model):
    followers = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    follower = models.ManyToManyField(Follower, null=True)
    following = models.ManyToManyField(Following, null=True)
    post = models.ManyToManyField(Post)
