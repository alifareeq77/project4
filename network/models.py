from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Following(models.Model):
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)


class Follower(models.Model):
    followers = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    follower = models.ManyToManyField(Follower)
    following = models.ManyToManyField(Following)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    post = models.CharField(max_length=15000)
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')

    def serialize(self):
        return {
            "id": self.id,
            'post':self.post
        }
