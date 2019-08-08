from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField
from Users.models import UserDetails

class FriendsFormedDetails(models.Model):
    user=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="logged_in_user")
    friend_name=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="current_user_friends")
    formedAt=models.DateTimeField(auto_now=True)
    friend_or_Request=models.BooleanField(default=False)
    access=models.CharField(max_length=10, default=None)

class UserFriends(models.Model):
    userId=models.OneToOneField(UserDetails, on_delete=models.CASCADE)
    friends=models.ManyToManyField(FriendsFormedDetails)