#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notifications
from .serializers import NotificationsSerializer
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
import json
from Users.models import UserDetails

#Get all Notes For A User
@api_view(['GET'])
def notification(request):
    permission_classes=(IsAuthenticated,)
    try:
        data=Notifications.objects.filter(toUser=UserDetails.objects.get(userId=request.user), isRead=False).order_by('-date')
        serializedData=NotificationsSerializer(data, many=True)
        return Response({'message':"Ok Done", "notifications": json.dumps(serializedData.data), "status":"200"})
    except Exception as e:
        print(e)
        return Response({'message':"Error", "status":"500"})

@api_view(['POST'])
def markAsRead(request):
    permission_classes=(IsAuthenticated,)
    try:
        for notif in Notifications.objects.filter(toUser=UserDetails.objects.get(userId=request.user), isRead=False):
            obj=Notifications.objects.get(id=notif.id)
            obj.isRead=True
            obj.save()
        return JsonResponse({"message":"Ok Saved", "status":"201"})

    except Exception as e:
        print(e)        
        return Response({'message':"Error", "status":"500"})