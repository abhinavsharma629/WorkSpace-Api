from django.db import models
from django.contrib.auth.models import User
from Users.models import UserDetails

class Notifications(models.Model):
    fromUser=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="from_user")
    toUser=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="to_user")
    notification=models.TextField()
    date=models.DateField(auto_now=True)
    isRead=models.BooleanField(default=False)