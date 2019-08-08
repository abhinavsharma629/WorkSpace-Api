from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FriendsFormedDetails, UserFriends
from .serializers import FriendsFormedDetailsSerializer, UserFriendsSerializer, UserSerializer
from django.utils import timezone
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
import requests
import time
import math
from django.http import JsonResponse
import json
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Polygon, MultiLineString, LineString, GEOSGeometry, MultiPoint, MultiPolygon
from django.db import connection
from Users.models import UserDetails
from Users.serializers import UserDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from functools import reduce
from operator import or_
from django.db.models import Q
from Shared.models import sharedNoteData, NotesDetails, CommentsOnNotes
from django_user_agents.utils import get_user_agent
from Notifications.models import Notifications
from Notifications.UserAgent import getDeviceDetails

class friendRecommendation(APIView):
    
    permission_classes= ((IsAuthenticated, ))
    def get(self,request):
		
        #Using Postgres earthdistance to find points lying within a given radius
        start=time.time() 
        pointsLyingInRange=UserDetails.objects.all()
            
        if(len(pointsLyingInRange)!=0):
                #Converting to POINT object
                #latitude=float(request.GET.get('lat'))
                #longitude=float(request.GET.get('long'))
                #radius=(int)(request.GET.get('radius'))
                obj=UserDetails.objects.get(userId=request.user)
                
                friendRequestSent=FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId=request.user), friend_or_Request=False)
                friendRequestReceived=FriendsFormedDetails.objects.filter(friend_name=UserDetails.objects.get(userId=request.user), friend_or_Request=False)
                friendsFormed=FriendsFormedDetails.objects.filter((Q(friend_name=UserDetails.objects.get(userId=request.user)) | Q(user=UserDetails.objects.get(userId=request.user))), friend_or_Request=True)
                serializer2= FriendsFormedDetailsSerializer(friendRequestSent, many=True)
                serializer3= FriendsFormedDetailsSerializer(friendRequestReceived, many=True)
                serializer4=FriendsFormedDetailsSerializer(friendsFormed, many=True)

                if(obj.current_lat and obj.current_long):
                    latitude=float(obj.current_lat)
                    longitude=float(obj.current_long)
                    radius=(int)(request.GET.get('distance'))
                    point='POINT('+str(latitude)+' '+str(longitude)+')'
                    pnt = GEOSGeometry(point, srid=4326)
                    
                    pointsLyingInRange = UserDetails.objects.filter(lat_long__distance_lte=(pnt, D(km=int(radius)))).exclude(userId=request.user)
                    #print(pointsLyingInRange)
                    #print(User.logged_in_user_set.filter(user__in=pointsLyingInRange))
                    #print(User.objects.filter(logged_in_user__in=pointsLyingInRange))
                    serializer= UserDetailsSerializer(pointsLyingInRange, many=True)
                    return JsonResponse({"ext_user":json.dumps(serializer.data), "sent":json.dumps(serializer2.data) , "received":json.dumps(serializer3.data), "friend":json.dumps(serializer4.data), "status": "200"})
                    
                else:
                    serializer= UserDetailsSerializer(UserDetails.objects.all().exclude(userId=request.user)[:10], many=True)  
                    return JsonResponse({"ext_user":json.dumps(serializer.data), "sent":json.dumps(serializer2.data) , "received":json.dumps(serializer3.data),"friend":json.dumps(serializer4.data), "status": "200"})
                    
        else:
                return Response({'Error Message':'Insufficient Data in Database'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def friendList(request):
    obj=UserDetails.objects.filter(userId__username__startswith=request.GET.get('suggest'))
    serializers=UserDetailsSerializer(obj, many=True)
    return JsonResponse({"suggestion_list":json.dumps(serializers.data), "status":"200"})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def createFriend(request):
    #Get User Agent Details
    params=request.data
    print(params)
    
    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)

    obj1, notif1=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=params['username']), notification=str(request.user.username+" Sent You A Request at from "+details))
    if(notif1):
        obj1.save()

    
    if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username'])).count()==0):
        obj, notif=FriendsFormedDetails.objects.get_or_create(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username']), access=params['access'])
        if(notif):
            obj.save()
            return JsonResponse({"message":"Ok Saved", "status": "200"})
        else:
            return JsonResponse({"message":"Error", "status": "500"})
    else:
        return JsonResponse({"message":"Already", "status": "400"})

@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def cancelRequest(request):
    params=request.data

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)
    
    obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=params['username']), notification=str(request.user.username+" canceled the Friend Request from "+details))
    if(notif):
        obj.save()

    print(params)
    if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username'])).count()==1):
        FriendsFormedDetails.objects.get(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username'])).delete()
        return JsonResponse({"message":"Ok Saved", "status": "200"})
    if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user)).count()==1):
        FriendsFormedDetails.objects.get(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user)).delete()
        return JsonResponse({"message":"Ok Saved", "status": "200"})
    else:
        return JsonResponse({"message":"Not Found", "status": "404"})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def removeFriend(request):
    params=request.data
    print(params)

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)

    obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=params['username']), notification=str(request.user.username+" unfriended you from "+details))
    if(notif):
        obj.save()

    try:
        if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username'])).count()==1):
            FriendsFormedDetails.objects.get(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=params['username'])).delete()
        
        if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user)).count()==1):
            FriendsFormedDetails.objects.get(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user)).delete()
        
        
        #Deleting Shared To From Notes Details For Current Both User and his friend
        sharedNoteData.objects.filter(sharedTo=UserDetails.objects.get(userId=request.user), noteId__userId=UserDetails.objects.get(userId__username=params['username'])).delete()
        sharedNoteData.objects.filter(sharedTo=UserDetails.objects.get(userId__username=params['username']), noteId__userId=UserDetails.objects.get(userId=request.user)).delete()

        #Deleting Comments From Notes Details For Current Both User and his friend
        [CommentsOnNotes.objects.get(noteId=likes['noteId']).delete() for likes in NotesDetails.objects.filter(admin=UserDetails.objects.get(userId=request.user), sharedTo__in=sharedNoteData.objects.filter(sharedTo__userId__username=params['username'])).values('noteId', 'comments')]
        [CommentsOnNotes.objects.get(noteId=likes['noteId']).delete() for likes in NotesDetails.objects.filter(admin=UserDetails.objects.get(userId__username=params['username']), sharedTo__in=sharedNoteData.objects.filter(sharedTo__userId=request.user)).values('noteId', 'comments')]
        
        #Deleting Likes From Notes Details For Current Both User and his friend
        [NotesDetails.objects.get(noteId=likes['noteId']).likes.remove(likes['likes']) for likes in NotesDetails.objects.filter(admin=UserDetails.objects.get(userId=request.user), sharedTo__in=sharedNoteData.objects.filter(sharedTo__userId__username=params['username'])).values('noteId', 'likes')]
        [NotesDetails.objects.get(noteId=likes['noteId']).likes.remove(likes['likes']) for likes in NotesDetails.objects.filter(admin=UserDetails.objects.get(userId__username=params['username']), sharedTo__in=sharedNoteData.objects.filter(sharedTo__userId=request.user)).values('noteId', 'likes')]
        
        return JsonResponse({"message":"Deleted", "status": "200"})
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Not Found", "status": "404"})


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def acceptFriend(request):
    params=request.data
    print(params)

    user_agent = get_user_agent(request)
    print(user_agent)
    details=getDeviceDetails(user_agent, request)


    obj,notif=Notifications.objects.get_or_create(fromUser=UserDetails.objects.get(userId=request.user), toUser=UserDetails.objects.get(userId__username=params['username']), notification=str(request.user.username+" Accepted Your Friend Request from "+details))
    if(notif):
        obj.save()


    if(FriendsFormedDetails.objects.filter(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user)).count()==1):
        print("inside none")
        friend=FriendsFormedDetails.objects.get(user=UserDetails.objects.get(userId__username=params['username']), friend_name=UserDetails.objects.get(userId=request.user))
        friend.friend_or_Request=True
        friend.save()
        print("saved")
        if(UserFriends.objects.filter(userId=UserDetails.objects.get(userId=request.user)).count()==0):
                obj1, notif1=UserFriends.objects.get_or_create(userId=UserDetails.objects.get(userId=request.user))
                if(notif1):
                    obj1.save()
                    obj1.friends.add(friend)
                    obj1.save()
                    print("saved1")
                    obj11, notif11=UserFriends.objects.get_or_create(userId=UserDetails.objects.get(userId__username=params['username']))
                    if(notif11):
                        obj11.save()
                        obj11.friends.add(friend)
                        obj11.save()
                        print("saved2")
                        return JsonResponse({"message":"Ok Saved", "status": "201"})
                    else:
                        return JsonResponse({"message":"Error", "status": "500"})
                else:
                    return JsonResponse({"message":"Error", "status": "500"})
        else:
            getUser=UserFriends.objects.get(userId=UserDetails.objects.get(userId=request.user))
            getUser.friends.add(friend)
            getUser.save()
            if(UserFriends.objects.filter(userId=UserDetails.objects.get(userId__username=params['username'])).count()==0):
                getUser1, notif1=UserFriends.objects.get_or_create(userId=UserDetails.objects.get(userId__username=params['username']))
                if(notif1):
                    getUser1.save()
                    getUser1.friends.add(friend)
                    getUser1.save()
                    return JsonResponse({"message":"Ok Saved", "status": "201"})
                else:
                    return JsonResponse({"message":"Error", "status": "500"})
            else:
                getUser1=UserFriends.objects.get(userId=UserDetails.objects.get(userId__username=params['username']))
                getUser1.friends.add(friend)
                getUser1.save()
                return JsonResponse({"message":"Ok Saved", "status": "201"})
    else:
        return JsonResponse({"message":"Not Found", "status": "404"})