#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import savedNoteData
from .serializers import savedNoteDataSerializer, savedNoteDataSerializer1
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import json
from Users.models import UserDetails
from django_user_agents.utils import get_user_agent
from Notifications.models import Notifications
from Notifications.UserAgent import getDeviceDetails
from Shared.models import NotesDetails
from rest_framework.parsers import JSONParser

#Save And Delete Your Note
class saveDeleteNote(APIView):
    permission_classes=(IsAuthenticated,)
    #GET NOTE
    def get(self, request):
        data=request.GET.get('noteId')
        print(data)
        try:
            notesData=savedNoteData.objects.get(noteId=data)
            serializer= savedNoteDataSerializer(notesData)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "No Such Note Present"}, status=status.HTTP_404_NOT_FOUND)

    permission_classes=(IsAuthenticated,)
    #POST SAVE
    def post(self, request, format=None):
        parser_classes = (MultiPartParser,)
        params=request.data

        print(params)

        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)

        if('caption' in params):
            obj,notif=savedNoteData.objects.get_or_create(userId=UserDetails.objects.get(userId=request.user), noteData=params['content'],typeOfData="note", title=params['title'], caption=params['caption'], createdFrom=details, showUpImg=params['imgData'], lastUpdated=timezone.now())
        else:
            obj,notif=savedNoteData.objects.get_or_create(userId=UserDetails.objects.get(userId=request.user), noteData=params['content'], typeOfData="note", title=params['title'], createdFrom=details, showUpImg=params['imgData'],  lastUpdated=timezone.now())
        if notif is True:
            obj.save()
            return JsonResponse({'message':"Ok Created", "status":"201", "id": obj.noteId, "date": obj.createdAt})
        else:
            return JsonResponse({'message':"Error", "status":"500"})

    permission_classes=(IsAuthenticated,)

    #DELETE
    def delete(self, request, format=None):
        params=request.data
        noteId=params['noteId']

        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)

        try:
            for users in NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=noteId)).sharedTo.all():
                print(users)
                obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=users.sharedTo.userId.username), notification=str(request.user.username+" deleted note with title:- "+savedNoteData.objects.get(noteId=noteId).title+" that was shared With You from "+details))
                if(notif):
                    obj.save()
        except Exception as e:
            print("No Shared Users")
        try:
            savedNoteData.objects.get(noteId=noteId).delete()
            return JsonResponse({"message": "Ok Deleted", "status":"200"})
        except Exception as e:
            print(e)
            stat=status.HTTP_404_NOT_FOUND
            return Response({"message": "Not Found", "status":"404"})

    permission_classes=(IsAuthenticated,)
    #PUT
    def put(self, request, format=None):
        params=request.data
        noteId=params['noteId']
        print(params['content'])


        user_agent = get_user_agent(request)
        print(user_agent)
        details=getDeviceDetails(user_agent, request)

        try:
            for users in NotesDetails.objects.get(noteId=savedNoteData.objects.get(noteId=noteId)).sharedTo.all():
                print(users)
                obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=users.sharedTo.userId.username), notification=str(request.user.username+" edited a note with title:- "+savedNoteData.objects.get(noteId=noteId).title+" that was shared With You from "+details))
                if(notif):
                    obj.save()
        except Exception as e:
            print(e)

        try:
            savedNoteData1=savedNoteData.objects.get(noteId=noteId)
            savedNoteData1.noteData=params['content']
            savedNoteData1.lastUpdated=timezone.now()
            savedNoteData1.save()
            return JsonResponse({"message": "Ok Edited", "status":"200"})
        except Exception as e:
            print(e)
            stat=status.HTTP_404_NOT_FOUND
            return Response({"message": "Not Found", "status":"404"})

#POST
@api_view(['POST'])
def editNote(request):
    permission_classes=(IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    params=request.data
    #user=params['user']
    noteId=params['noteId']
    file=params['file']
    print(noteId)
    try:
        obj=savedNoteData.objects.get(noteId=noteId)
        print(obj)
        obj.noteData=file
        obj.lastUpdated=timezone.now()
        obj.save()
        stat=status.HTTP_201_CREATED
        return Response({'message':"Ok Done", 'data':serializers.serialize('json',savedNoteData.objects.filter(noteId=noteId))}, status=stat)
    except Exception as e:
        print(e)
        stat=status.HTTP_404_NOT_FOUND
        return Response({'message':"Error"}, status=stat)

    #To serialize all data of the particular user at once
    # serializer = serializers.serialize('json', savedNoteData.objects.all(), fields=('noteId', 'username','noteData', 'createdAt', 'lastUpdated'))

    # print(serializer)
    # return Response(serializer, status=stat)


#Get all Notes For A User
@api_view(['GET'])
def getAllNotes(request):
    permission_classes=(IsAuthenticated,)
    try:
        data=savedNoteData.objects.filter(userId=UserDetails.objects.get(userId=request.user), typeOfData="note").order_by('-createdAt')
        serializedData=savedNoteDataSerializer(data, many=True)
        return Response({'message':"Ok Done", "data": json.dumps(serializedData.data), "status":"200"})
    except Exception as e:
        print(e)
        return Response({'message':"Error", "status":"500"})


#Get all Notes For A User
@api_view(['GET'])
def getAllNotesWithLessData(request):
    permission_classes=(IsAuthenticated,)
    try:
        data=savedNoteData.objects.filter(userId=UserDetails.objects.get(userId=request.user), typeOfData="note").order_by('-createdAt')
        serializedData=savedNoteDataSerializer1(data, many=True)
        return Response({'message':"Ok Done", "data": json.dumps(serializedData.data), "status":"200"})
    except Exception as e:
        print(e)
        return Response({'message':"Error", "status":"500"})



@api_view(['POST'])
def submitGitHubNote(request):
    permission_classes=(IsAuthenticated,)
    parser_classes = [JSONParser]


    params=request.data

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)

    #print(params['content'])
    #print(type(params['content']))
    js=json.loads(params['content'])
    print(js)
    print(type(js))
    if('caption' in params):
        obj,notif=savedNoteData.objects.get_or_create(userId=UserDetails.objects.get(userId=request.user), gitHubData=json.loads(params['content']), typeOfData="git" , title=params['title'], caption=params['caption'], createdFrom=details, lastUpdated=timezone.now())
    else:
        obj,notif=savedNoteData.objects.get_or_create(userId=UserDetails.objects.get(userId=request.user), gitHubData=json.loads(params['content']), typeOfData="git" , title=params['title'], createdFrom=details,   lastUpdated=timezone.now())
    if notif is True:
        obj.save()
        import requests
        print(request.META.get('HTTP_AUTHORIZATION'))

        url="https://shielded-dusk-55059.herokuapp.com/shared/shareNote/"
        res=requests.post(url, data={
            "list[]":request.data['list[]'],
            "noteId":obj.noteId
        }, headers={
            "Authorization": request.META.get('HTTP_AUTHORIZATION')
        }).json()

        if(res['status']=="201"):
            return JsonResponse({'message':"Ok Created", "status":"201", "id": obj.noteId, "date": obj.createdAt})
        else:
            return JsonResponse({'message':"Error", "status":"500"})
    else:
        return JsonResponse({'message':"Error", "status":"500"})
