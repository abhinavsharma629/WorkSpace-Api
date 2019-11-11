#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import sharedNoteData, CommentsOnNotes, NotesDetails
from .serializers import sharedNoteDataSerializer, CommentsOnNotesSerializer, NotesDetailsSerializer, sharedNotesWithoutDetailsSerializer
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import json
from PersonalNotes.models import savedNoteData
from Friends.models import UserFriends
from Friends.serializers import FriendsFormedDetailsSerializer
from Users.models import UserDetails
from Users.serializers import UserDetailsSerializer
from django_user_agents.utils import get_user_agent
from Notifications.models import Notifications
from Notifications.UserAgent import getDeviceDetails
from Friends.serializers import UserFriendsSerializer, UserFriendsWithDetailsSerializer, FriendsFormedDetailsSerializer, UserFriendsSerializer
from socialmediaAuthentica.models import CloudOauth2Details

@api_view(['POST'])
def shareNote(request):
    permission_classes=(IsAuthenticated,)

    print(request.POST)
    print("\n\n")
    print(request.data)
    friends=request.data.get('list[]')
    print(request.data.get('list[]'), request.data.get('noteId'))

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)

    '''May Fail in cases like if a user changes his/her username
    sharedNoteData.objects.bulk_create(
        [sharedNoteData(noteId=savedNoteData.objects.get(noteId=request.POST.get('noteId')), admin=User.objects.get(username=request.user.username), sharedTo=User.objects.get(username=currName)) for currName in friends]
     ) '''
    try:
        for currName in friends:

            obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=currName), notification=str(request.user.username+" shared a note With You from"+details))
            if(notif):
                obj.save()

            obj,notif=sharedNoteData.objects.get_or_create(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId')), sharedTo=UserDetails.objects.get(userId__username=currName), sharedFrom=details)
            if(notif):
                obj.save()
                if(NotesDetails.objects.filter(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId'))).count()==0):
                    obj1, notif1=NotesDetails.objects.get_or_create(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId')), admin=UserDetails.objects.get(userId=request.user))
                    if(notif1):
                        obj1.save()
                        obj1.sharedTo.add(obj)
                        obj1.save()
                        return JsonResponse({"message":"Ok Shared", "status":"201"})
                    else:
                        return JsonResponse({"message":"Error", "status":"500"})
                else:
                    getNote=NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId')))
                    getNote.sharedTo.add(obj)
                    getNote.save()
                    return JsonResponse({"message":"Ok Shared", "status":"201"})
        return JsonResponse({"message":"Ok Shared", "status":"201"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"500"})


@api_view(['DELETE'])
def deleteSharedNote(request):
    permission_classes=(IsAuthenticated,)

    friends=request.data.get('list[]')
    print(request.data.get('list[]'), request.data.get('noteId'))

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)

    try:
        for currName in friends:
            obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=currName), notification=str(request.user.username+" deleted a shared note from"+details))
            if(notif):
                obj.save()
            sharedNoteData.objects.get(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId')), sharedTo=UserDetails.objects.get(userId__username=currName)).delete()
            NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId'))).comments.filter(userId=UserDetails.objects.get(userId__username=currName)).delete()
            [NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId'))).likes.remove(user) for user in NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=request.data.get('noteId'))).likes.filter(userId=User.objects.get(username=currName))]

        return JsonResponse({"message":"Ok Shared", "status":"200"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"500"})


@api_view(['GET'])
def noteSharedTo(request):
    permission_classes=(IsAuthenticated,)

    try:
        sharedUsers=sharedNoteData.objects.filter(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId')))
        serializers=sharedNoteDataSerializer(sharedUsers, many=True)

        return JsonResponse({"sharedTo":json.dumps(serializers.data), "status":"200"})

    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"500"})


@api_view(['GET'])
def getFriends(request):
    permission_classes=(IsAuthenticated,)

    print(request.GET)
    print("\n\n")
    print(request.data)
    shared=sharedNoteData.objects.filter(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId')))
    print(shared)

    serializers1=sharedNoteDataSerializer(shared, many=True)
    print(json.dumps(serializers1.data, indent=4))

    if(UserFriends.objects.filter(userId=UserDetails.objects.get(userId=request.user)).count()>0):

        print(sharedNoteData.objects.filter(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId'))).values('sharedTo'))
        print(UserFriends.objects.get(userId=UserDetails.objects.get(userId=request.user)).friends)
        sharedUsers=UserFriends.objects.get(userId=UserDetails.objects.get(userId=request.user)).friends.exclude(friend_name_id__in=sharedNoteData.objects.filter(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId'))).values('sharedTo'))

        print(sharedUsers)
        serializers=FriendsFormedDetailsSerializer(sharedUsers, many=True)
        print(json.dumps(serializers.data, indent=4))
        return JsonResponse({"list":json.dumps(serializers.data) ,"status": "200"})
    else:
        return JsonResponse({"message":"No Friends Present" , "status": "404"})
    # if(UserFriends.objects.filter(userId=request.user).count()>0):
    #     obj=UserFriends.objects.get(userId=request.user)
    #     print(obj)
    #     friendsList=obj.friends.all()
    #     serializer=FriendsFormedDetailsSerializer(friendsList, many=True)
    #     return JsonResponse({"list":json.dumps(serializer.data), "status": "200"})
    # else:
    #     return JsonResponse({"message":"No Friends", "status": "404"})

@api_view(['GET'])
def sharedNotes(request):
    permission_classes=(IsAuthenticated,)
    sharedNotes=sharedNoteData.objects.filter(sharedTo=UserDetails.objects.get(userId=request.user)).select_related()
    print(sharedNotes)
    #serializers=sharedNoteDataSerializer(sharedNotes, many=True)

    #return JsonResponse({"sharedNotes":json.dumps(serializers.data) ,"status": "200"})
    return JsonResponse({"status": "200"})

class likeOnNote(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request):

        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)



        print(NotesDetails.objects.get(noteId=request.data['noteId']).likes.all())
        if(not UserDetails.objects.get(userId=request.user) in NotesDetails.objects.get(noteId=request.data['noteId']).likes.all()):

            #Like Notif to Admin
            if(request.user.username!=NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username):
                obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=NotesDetails.objects.get(noteId=request.data['noteId']).admin, notification=str(request.user.username+" liked note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
                if(notif):
                    obj.save()

            #Like Notif To All Users To Whom The Note Is Shared
            for currUser in NotesDetails.objects.get(noteId=request.data['noteId']).sharedTo.all():
                print(currUser.sharedTo.userId.username, request.user.username)
                if(currUser.sharedTo.userId.username!= request.user.username):
                    obj1,notif1=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=currUser.sharedTo, notification=str(request.user.username+" liked note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
                    if(notif1):
                        obj1.save()

            obj1=NotesDetails.objects.get(noteId=request.data['noteId'])
            obj1.likes.add(UserDetails.objects.get(userId=request.user))
            obj1.likesCount+=1
            obj1.save()
            return JsonResponse({"message":"Created" ,"status": "201"})

    permission_classes=(IsAuthenticated,)
    def delete(self, request):
        print("inside")
        print(request.data)

        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)

        if(request.user.username!=NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username):
            #Disike Comment to Note Admin
            obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=NotesDetails.objects.get(noteId=request.data['noteId']).admin, notification=str(request.user.username+" disliked the note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
            if(notif):
                obj.save()

        #Dislike Notif To All Users To Whom The Note Is Shared
        for currUser in NotesDetails.objects.get(noteId=request.data['noteId']).sharedTo.all():
            print(currUser.sharedTo.userId.username, request.user.username)
            if(currUser.sharedTo.userId.username!= request.user.username):
                obj1,notif1=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=currUser.sharedTo, notification=str(request.user.username+" disliked note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
                if(notif1):
                    obj1.save()

        like=NotesDetails.objects.get(noteId=request.data['noteId'])
        like.likesCount-=1
        like.likes.remove(UserDetails.objects.get(userId=request.user))
        like.save()
        return JsonResponse({"message":"Removed" ,"status": "200"})


class commentOnNote(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request):


        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)

        #Comment Notif To Note Admin
        if(request.user.username!=NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username):
            obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=NotesDetails.objects.get(noteId=request.data['noteId']).admin, notification=str(request.user.username+" commented '"+request.data['comment'][0:10]+"...' on the note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
            if(notif):
                obj.save()

        #Comment Notif To All Users To Whom The Note Is Shared
        for currUser in NotesDetails.objects.get(noteId=request.data['noteId']).sharedTo.all():
            print(currUser.sharedTo.userId.username, request.user.username)
            if(currUser.sharedTo.userId.username!= request.user.username):
                obj1,notif1=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=currUser.sharedTo, notification=str(request.user.username+" commented '"+request.data['comment'][0:10]+"...' on the note with title:- "+NotesDetails.objects.get(noteId=request.data['noteId']).noteId.title+" that was shared by "+NotesDetails.objects.get(noteId=request.data['noteId']).admin.userId.username+" from "+details))
                if(notif1):
                    obj1.save()


        comment, notif=CommentsOnNotes.objects.get_or_create(noteId=savedNoteData(noteId=request.data['noteId']), userId=UserDetails.objects.get(userId=request.user), comment=request.data['comment'])
        if(notif):
            comment.save()
            obj=NotesDetails.objects.get(noteId=request.data['noteId'])
            obj.comments.add(comment)
            obj.save()
            return JsonResponse({"message":"Created" ,"status": "201", "generatedId":comment.commentId})
        else:
            return JsonResponse({"message":"Error" ,"status": "500"})

    permission_classes=(IsAuthenticated,)
    def delete(self, request):
        CommentsOnNotes.objects.get(commentId=request.data['commentId']).delete()
        return JsonResponse({"message":"Removed" ,"status": "200"})


@api_view(['GET'])
def noteDetails(request):
    permission_classes=(IsAuthenticated,)

    sharedNotesForCurrentUser=NotesDetails.objects.filter(sharedTo__sharedTo__userId__exact=UserDetails.objects.get(userId=request.user).userId)
    serializers=NotesDetailsSerializer(sharedNotesForCurrentUser, many=True)

    likesNotesForCurrentUser=NotesDetails.objects.filter(likes__userId=request.user)
    likes_serializer=NotesDetailsSerializer(likesNotesForCurrentUser, many=True)

    sharedDetails=sharedNoteData.objects.filter(sharedTo=UserDetails.objects.get(userId=request.user))
    print(sharedDetails)
    serializers1=sharedNotesWithoutDetailsSerializer(sharedDetails, many=True)
    return JsonResponse({"message": "Ok", "sharedNotes": json.dumps(serializers.data),"sharedDetails": json.dumps(serializers1.data),"likedNotes":json.dumps(likes_serializer.data), "status": "200"})



@api_view(['GET'])
def selfSharedNoteDetails(request):
    permission_classes=(IsAuthenticated,)

    sharedNotesForCurrentUser=NotesDetails.objects.filter(admin=UserDetails.objects.get(userId=request.user))
    serializers=NotesDetailsSerializer(sharedNotesForCurrentUser, many=True)
    print(serializers.data)

    likesNotesForCurrentUser=NotesDetails.objects.filter(likes__userId=request.user)
    likes_serializer=NotesDetailsSerializer(likesNotesForCurrentUser, many=True)
    #print(likes_serializer.data)

    sharedDetails=sharedNoteData.objects.filter(noteId__userId=UserDetails.objects.get(userId=request.user))
    #print(sharedDetails)
    serializers1=sharedNotesWithoutDetailsSerializer(sharedDetails, many=True)
    return JsonResponse({"message": "Ok", "sharedNotes": json.dumps(serializers.data),"sharedDetails": json.dumps(serializers1.data),"likedNotes":json.dumps(likes_serializer.data), "status": "200"})


@api_view(['GET'])
def specificNoteDetail(request):
    permission_classes=(IsAuthenticated,)

    print(request.GET.get('noteId'))
    sharedNotesForCurrentUser=NotesDetails.objects.filter(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId')))
    serializers=NotesDetailsSerializer(sharedNotesForCurrentUser, many=True)

    return JsonResponse({"message": "Ok", "noteDetails": json.dumps(serializers.data), "status": "200"})


@api_view(['GET'])
def specificNoteDetailForGit(request):
    permission_classes=(IsAuthenticated,)

    print(request.GET.get('noteId'))

    sharedNotesForCurrentUser=NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=request.GET.get('noteId')))
    serializers=NotesDetailsSerializer(sharedNotesForCurrentUser)


    return JsonResponse({"message": "Ok", "noteDetails": json.dumps(serializers.data),"gitHubData":json.dumps(sharedNotesForCurrentUser.noteId.gitHubData), "status": "200"})

@api_view(['GET'])
def allUserFriends(request):
    try:
        friends=UserFriends.objects.get(userId=UserDetails.objects.get(userId=request.user)).friends.all()

        print(friends)
        serializer=FriendsFormedDetailsSerializer(friends, many=True)
        print(serializer.data)
        return JsonResponse({"list": json.dumps(serializer.data), "status":"200"})

    except Exception as e:
        return JsonResponse({"message": "No Friends", "status":"404"})
