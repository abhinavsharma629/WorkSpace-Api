from rest_framework import serializers
from PersonalNotes.models import savedNoteData
from .models import sharedNoteData, CommentsOnNotes, NotesDetails
from Users.serializers import UserDetailsSerializer

class sharedNoteDataSerializer(serializers.ModelSerializer):
    shared_to=serializers.CharField(source='sharedTo.userId')
    admin=serializers.CharField(source='noteId.userId.userId.username')
    noteId=serializers.CharField(source='noteId.noteId')
    noteData=serializers.CharField(source='noteId.noteData')
    gitHubData=serializers.CharField(source="noteId.gitHubData")
    typeOfData=serializers.CharField(source="noteId.typeOfData")
    note_created_date=serializers.CharField(source='noteId.createdAt')
    note_last_updated=serializers.CharField(source='noteId.lastUpdated')
    admin_profile_picture=serializers.CharField(source='noteId.userId.profilePhoto')
    occupation=serializers.CharField(source='noteId.userId.occupation')

    class Meta:
      model=sharedNoteData  # what module you are going to serialize
      fields= ('noteData', 'noteId', 'note_created_date', 'note_last_updated', 'shared_to', 'admin', 'sharedAt', 'admin_profile_picture', 'occupation', 'gitHubData', 'typeOfData')


class CommentsOnNotesSerializer(serializers.ModelSerializer):
  user=serializers.CharField(source='userId.userId.username')

  class Meta:
    model=CommentsOnNotes  # what module you are going to serialize
    fields= ('commentId', 'user', 'comment', 'timeOfComment', 'userAgent')



class CommentsOnNotesSerializerWithoutDetails(serializers.ModelSerializer):
    user=serializers.CharField(source='userId.userId.username')
    class Meta:
        model=CommentsOnNotes  # what module you are going to serialize
        fields= ('commentId', 'user')


class sharedNotesWithoutDetailsSerializer(serializers.ModelSerializer):
  noteId=serializers.CharField(source='noteId.noteId')
  receiver=serializers.CharField(source='sharedTo.userId')
  receiver_profilePhoto=serializers.CharField(source='sharedTo.profilePhoto')

  class Meta:
    model=sharedNoteData
    fields=('noteId', 'receiver', 'sharedAt', 'receiver_profilePhoto', 'sharedFrom')

class NotesDetailsSerializer(serializers.ModelSerializer):
  note_id=serializers.CharField(source='noteId.noteId')
  noteTitle=serializers.CharField(source='noteId.title')
  noteCaption=serializers.CharField(source='noteId.caption')
  createdFrom=serializers.CharField(source='noteId.createdFrom')
  showUpImg=serializers.CharField(source='noteId.showUpImg')
  note_admin=serializers.CharField(source='admin.userId.username')
  noteData=serializers.CharField(source='noteId.noteData')
  gitHubData=serializers.CharField(source="noteId.gitHubData")
  typeOfData=serializers.CharField(source="noteId.typeOfData")
  note_created_date=serializers.CharField(source='noteId.createdAt')
  note_last_updated=serializers.CharField(source='noteId.lastUpdated')
  admin_profile_picture=serializers.CharField(source='noteId.userId.profilePhoto')
  occupation=serializers.CharField(source='noteId.userId.occupation')
  likes=UserDetailsSerializer(many=True)
  comments=CommentsOnNotesSerializer(many=True)

  class Meta:
    model=NotesDetails
    fields=('note_id', 'note_admin', 'noteTitle', 'noteCaption', 'createdFrom', 'showUpImg', 'noteData','gitHubData', 'typeOfData' , 'note_created_date', 'note_last_updated', 'admin_profile_picture', 'occupation', 'comments', 'likesCount', 'likes')


class NotesDetailsSerializerForPosts(serializers.ModelSerializer):
  note_id=serializers.CharField(source='noteId.noteId')
  noteTitle=serializers.CharField(source='noteId.title')
  noteCaption=serializers.CharField(source='noteId.caption')
  createdFrom=serializers.CharField(source='noteId.createdFrom')
  showUpImg=serializers.CharField(source='noteId.showUpImg')
  note_admin=serializers.CharField(source='admin.userId.username')
  typeOfData=serializers.CharField(source="noteId.typeOfData")
  note_created_date=serializers.CharField(source='noteId.createdAt')
  note_last_updated=serializers.CharField(source='noteId.lastUpdated')
  admin_profile_picture=serializers.CharField(source='noteId.userId.profilePhoto')
  occupation=serializers.CharField(source='noteId.userId.occupation')
  likes=UserDetailsSerializer(many=True)
  comments=CommentsOnNotesSerializerWithoutDetails(many=True)

  class Meta:
    model=NotesDetails
    fields=('note_id', 'note_admin', 'noteTitle', 'noteCaption', 'createdFrom', 'showUpImg', 'typeOfData' , 'note_created_date', 'note_last_updated', 'admin_profile_picture', 'occupation', 'comments', 'likesCount', 'likes')


class NotesDetailsSerializerForLikes(serializers.ModelSerializer):
  note_id=serializers.CharField(source='noteId.noteId')

  class Meta:
    model=NotesDetails
    fields=('note_id', 'likesCount')



class NotesDetailsSerializerForComments(serializers.ModelSerializer):
  note_id=serializers.CharField(source='noteId.noteId')
  noteTitle=serializers.CharField(source='noteId.title')
  comments=CommentsOnNotesSerializer(many=True)

  class Meta:
    model=NotesDetails
    fields=('note_id', 'noteTitle', 'comments')
