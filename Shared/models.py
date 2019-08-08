from django.db import models
from django.contrib.auth.models import User
from Users.models import UserDetails
from PersonalNotes.models import savedNoteData


class CommentsOnNotes(models.Model):
    commentId=models.AutoField(primary_key=True)
    noteId=models.ForeignKey(savedNoteData, on_delete=models.CASCADE)
    userId=models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    timeOfComment=models.DateField(auto_now=True)
    comment=models.TextField()
    userAgent=models.CharField(max_length=100, null=True, blank=True)

class sharedNoteData(models.Model):
    noteId=models.ForeignKey(savedNoteData, on_delete=models.CASCADE)
    sharedTo= models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="shared_to")
    sharedAt=models.DateTimeField(auto_now=True)
    sharedFrom=models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = (("noteId", "sharedTo"),)

class NotesDetails(models.Model):
    noteId=models.ForeignKey(savedNoteData, on_delete=models.CASCADE)
    admin=models.ForeignKey(UserDetails, on_delete=models.CASCADE, related_name="note_admin")
    comments=models.ManyToManyField(CommentsOnNotes, blank=True)
    likes=models.ManyToManyField(UserDetails, blank=True)
    likesCount=models.PositiveIntegerField(default=0)
    sharedTo=models.ManyToManyField(sharedNoteData)