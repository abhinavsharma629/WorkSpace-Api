from django.core import serializers
from .models import UserDetails
from .serializers import UserDetailsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.utils.dateparse import parse_date
import requests
from django_user_agents.utils import get_user_agent
from Notifications.models import Notifications
from Notifications.UserAgent import getDeviceDetails
# import logging

# logger=logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes((IsAuthenticated, )) #For @api_view
def getUserDetails(request, format=None):
    # try:
    #     div=1/0
    # except Exception as e:
    #     logger.error(str(e))
    #print(1/0)
    
    print(request.user.username)
    try:
        extendedData=UserDetails.objects.get(userId=request.user)
        data=User.objects.filter(username=request.user.username)
        serializedData=UserDetailsSerializer(extendedData)
        data=serializers.serialize('json', data)
        return Response({"message":"Ok Done", 'data':data, 'extendedData':serializedData.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    
    # extendedData=UserDetails.objects.get(userId=request.user)
    # data=User.objects.filter(username=request.user.username)
    # serializedData=UserDetailsSerializer(extendedData)
    # data=serializers.serialize('json', data)
    # return Response({"message":"Ok Done", 'data':data, 'extendedData':serializedData.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def editUserDetails(request, format=None):
    #permission_classes=(IsAuthenticated,)
    parser=(MultiPartParser,)

    obj=UserDetails.objects.get(userId=request.user)
    obj1=User.objects.get(username=request.user.username)
    try:
        params=request.data
        if('email' in params):
            try:
                obj1.email=params['email']
            except:
                return Response({"message": "Error in Email Address"}, status=status.HTTP_404_NOT_FOUND)

        if('first_name' in params):
            try:
                obj1.email=params['first_name']
            except:
                return Response({"message": "Error in First Address"}, status=status.HTTP_404_NOT_FOUND)
        
        if('last_name' in params):
            try:
                obj1.email=params['last_name']
            except:
                return Response({"message": "Error in Last Address"}, status=status.HTTP_404_NOT_FOUND)

        
        if('address' in params):
            try:
                obj.address=params['address']
            except:
                return Response({"message": "Error in Address"}, status=status.HTTP_404_NOT_FOUND)
        
        if('address1' in params):
            try:
                obj.address1=params['address1']
            except:
                return Response({"message": "Error in Address 1"}, status=status.HTTP_404_NOT_FOUND)
        
        if('phoneNumber' in params):
            try:
                obj.phoneNumber=params['phoneNumber']
            except:
                return Response({"message": "Error in Phone Number"}, status=status.HTTP_404_NOT_FOUND)
        
        if('alternatePhoneNumber' in params):
            try:
                obj.alternatePhoneNumber=params['alternatePhoneNumber']
            except:
                return Response({"message": "Error in Alternate Phone Number"}, status=status.HTTP_404_NOT_FOUND)
        
        if('profilePic' in params):
            try:
                obj.profilePhoto=params['profilePic']
            except:
                return Response({"message": "Error in Profile Pic"}, status=status.HTTP_404_NOT_FOUND)
        
        if('coverPic' in params):
            try:
                obj.alternatePhoneNumber=params['coverPic']
            except:
                return Response({"message": "Error in Cover Pic"}, status=status.HTTP_404_NOT_FOUND)
        
        if('date' in params):
            try:
                obj.dateOfBirth=params['date']
            except:
                return Response({"message": "Error in Date"}, status=status.HTTP_404_NOT_FOUND)
        
        if('gender' in params):
            try:
                obj.gender=params['gender']
            except:
                return Response({"message": "Error in Gender"}, status=status.HTTP_404_NOT_FOUND)
        
        if('email1' in params):
            try:
                obj.alternateEmailAddress=params['email']
            except:
                return Response({"message": "Error in Alternate Email Address"}, status=status.HTTP_404_NOT_FOUND)
        
        obj.save()
        obj1.save()
        serializedData=UserDetailsSerializer(obj)
        return Response({"message":"Ok Done", 'data':serializedData.data}, status=status.HTTP_200_OK)
    except:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def deleteUserDetails(request, format=None):
    # permission_classes=(IsAuthenticated,)
    try:
        UserDetails.objects.get(userId=request.user).delete()
        return Response({"message":"Ok Done"}, status=status.HTTP_200_OK)
    except:
        return Response({"message":"Not Found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def createUser(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(params)
    
    try:
        obj,notif=User.objects.get_or_create(username=params['username'], email=params['email'])
        obj.set_password(params['pass'])
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"304"})
    if(notif):
        obj.save()
        obj.firstname=params['fname']
        obj.lastname=params['lname']
        obj.save()
        
        date = parse_date(params['dob'])
        
        obj1,notif1=UserDetails.objects.get_or_create(userId=User.objects.get(username=params['username']), address=params['address'], address1=params['address1'], phoneNumber=params['phone'], occupation=params['occupation'], state=params['state'], city=params['city'], country=params['country'], alternatePhoneNumber=params['phone1'], dateOfBirth=date, gender=params['gender'],current_lat=(float)(params['lat']), current_long=(float)(params['long']))
        if(notif1):
            obj1.save()
            obj1.lat_long='POINT('+str(params['lat'])+' '+str(params['long'])+')'
            obj1.profilePhoto=params['file']
            #obj1.coverPhoto=params['file1']
            obj1.save()
            res=requests.post('http://127.0.0.1:8000/user/api/token/', data={'username': params['username'], 'password': params['pass']}).json()
            print(res)
            return JsonResponse({"message":"Success", "status":"201", 'token_data': res})
        else:
            return JsonResponse({"message":"Error", "status":"203"})
       
        
    else:
        return JsonResponse({"message":"Error", "status":"203"})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def validateUser(request, format=None):
    params=request.data
    print(params)
    user=authenticate(username=params['username'], password=params['pass'])
    print(user)
    if(user is not None):
        res=requests.post('http://127.0.0.1:8000/user/api/token/', data={'username': params['username'], 'password': params['pass']}).json()
        return JsonResponse({"message": "Success", "status":"200", 'token_data': res})
    else:
        return JsonResponse({"message": "Success", "status":"404"})