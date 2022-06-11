from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


"""
# one-sided relation
if user is following someone will create table with user name that is followed and user is following
if we want to get the followed user we will filter by  followed_user and that doesn't mean that the 
followed user is following the user who followed him
"""


class Following(models.Model):
    followed_by = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
        }


class Post(models.Model):
    post = models.CharField(max_length=15000)
    date = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_profile')

    def serialize(self):
        return {
            "id": self.id,
            'post': self.post
        }


class Likes(models.Model):
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE)
