from django.db import models
from django.contrib.auth.models import User
from Users.models import UserDetails
from django.contrib.postgres.fields import JSONField

class savedNoteData(models.Model):
    noteId=models.AutoField(primary_key=True)
    userId= models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    noteData=models.TextField()

    #-------------------------------------------------
    # Seperate This Later To Another Model
    gitHubData=JSONField(null=True, blank=True)
    typeOfData=models.CharField(max_length=100, null=True, blank=True)
    #-------------------------------------------------

    title=models.CharField(max_length=1000)
    caption=models.TextField(null=True, blank=True)
    createdFrom=models.CharField(max_length=100, null=True, blank=True)
    showUpImg=models.TextField(null=True, blank=True)
    #showUpImg1=models.FileField(upload_to='notes_pictures', null=True, blank=True)
    createdAt=models.DateTimeField(auto_now=True)
    lastUpdated=models.DateTimeField()
