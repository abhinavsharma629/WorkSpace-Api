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
from Friends.models import FriendsFormedDetails, UserFriends
from django.contrib.auth.hashers import check_password
from Shared.models import NotesDetails

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


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def profileShowDetails(request, format=None):
    details=UserDetails.objects.get(userId=request.user)
    username=request.user.username
    full_name=request.user.first_name+" "+request.user.last_name
    img_url=details.profilePhoto.url
    occupation=details.occupation
    total_friends=UserFriends.objects.get(userId=UserDetails.objects.get(userId=request.user)).friends.all().count()
    curr_lat=details.current_lat
    curr_long=details.current_long

    return JsonResponse({"username":username, "img_url":img_url ,"name":full_name, "occupation":occupation, "total_friends":total_friends, "curr_lat":curr_lat, "curr_long":curr_long, "status":"200"})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def friendShowDetails(request, format=None):
    details=UserDetails.objects.get(userId__username=request.GET.get('username'))
    username=request.GET.get('username')
    full_name=User.objects.get(username=request.GET.get('username')).first_name+" "+User.objects.get(username=request.GET.get('username')).last_name
    img_url=details.profilePhoto.url
    occupation=details.occupation
    total_friends=UserFriends.objects.get(userId=UserDetails.objects.get(userId__username=request.GET.get('username'))).friends.all().count()
    curr_lat=details.current_lat
    curr_long=details.current_long
    if(FriendsFormedDetails.objects.filter(Q(user__userId__username=request.GET.get('username')) | Q(friend_name__userId__username=request.GET.get('username'))).count()>0):
        obj=FriendsFormedDetails.objects.get(Q(user__userId__username=request.GET.get('username'), friend_name__userId__username=request.user.username) | Q(friend_name__userId__username=request.GET.get('username'), user__userId__username=request.user.username))
        formedAt=obj.formedAt
        isFriend=obj.friend_or_Request
    total_notes=NotesDetails.objects.filter(admin__userId__username=request.GET.get('username')).count()

    curr_ShowUserFriends=FriendsFormedDetails.objects.filter(Q(user__userId__username=request.GET.get('username'), friend_or_Request=True)).values('friend_name__userId')
    curr_ShowUserFriends1=FriendsFormedDetails.objects.filter(Q(friend_name__userId__username=request.GET.get('username'), friend_or_Request=True)).values('user__userId')

    mutual_friends=FriendsFormedDetails.objects.filter(Q(friend_name__userId__username=request.user.username, user__userId__in=curr_ShowUserFriends) | Q(friend_name__userId__in=curr_ShowUserFriends, user__userId__username=request.user.username)).count()
    mutual_friends1=FriendsFormedDetails.objects.filter(Q(friend_name__userId__username=request.user.username, user__userId__in=curr_ShowUserFriends1) | Q(friend_name__userId__in=curr_ShowUserFriends1, user__userId__username=request.user.username)).count()
    print(mutual_friends, mutual_friends1)

    return JsonResponse({"username":username, "img_url":img_url ,"name":full_name, "occupation":occupation, "total_friends":total_friends, "curr_lat":curr_lat, "curr_long":curr_long, "mutual":mutual_friends, "mutual1":mutual_friends1, "status":"200"})



@api_view(['GET'])
@permission_classes((IsAuthenticated, )) #For @api_view
def userValidity(request):
    if(User.objects.filter(username=request.GET.get('username')).count()==1):
        isFriends=False
        userImgUrl=UserDetails.objects.get(userId__username=request.GET.get('username')).profilePhoto.url
        print(userImgUrl)
        if(FriendsFormedDetails.objects.filter(Q(user=UserDetails.objects.get(userId__username=request.GET.get('username')), friend_name=UserDetails.objects.get(userId=request.user)) | Q(user=UserDetails.objects.get(userId=request.user), friend_name=UserDetails.objects.get(userId__username=request.GET.get('username')))).count()>0):
            isFriends=True
        return JsonResponse({'message':"User Found", 'isFriends':isFriends,"userImg":userImgUrl, "status":"200"})

    else:
        return JsonResponse({'message':"Error", 'status':'404'})


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
            res=requests.post('https://shielded-dusk-55059.herokuapp.com/user/api/token/', data={'username': params['username'], 'password': params['pass']}).json()
            print(res)
            return JsonResponse({"message":"Success", "status":"201", 'token_data': res})
        else:
            return JsonResponse({"message":"Error", "status":"203"})


    else:
        return JsonResponse({"message":"Error", "status":"203"})

#TEST TO SAVE IMAGE FROM REACT NATIVE
@api_view(['POST'])
@permission_classes((AllowAny, ))
def saveImage(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    print(request.FILES)
    print(params)

    import uuid
    randomName=str(uuid.uuid1())
    obj,notif=User.objects.get_or_create(username=randomName, email="abhinavsharma622@gmail.com")
    obj.set_password("abhi629@@")
    if(notif):
        obj.save()
        date = parse_date("2019-08-09")
        obj1,notif1=UserDetails.objects.get_or_create(userId=User.objects.get(username=randomName), address="sddsfsfsdfs", address1="asdadsadsad", phoneNumber="7909948987", occupation="sdffffffff", state="ads", city="ads", country="asd", alternatePhoneNumber="9557806467", dateOfBirth=date, gender="M")
        if(notif1):
            obj1.save()
            obj1.lat_long='POINT('+str("23.56")+' '+str("34.67")+')'
            obj1.profilePhoto=request.FILES['photo']
            obj1.save()
            return JsonResponse({"img":obj1.profilePhoto.url, "status":"201"})
        else:
            return JsonResponse({"status":"500"})
    else:
        return JsonResponse({"status":"404"})



@api_view(['POST'])
@permission_classes((AllowAny, ))
def createFullUser(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    pic=request.FILES['photo']
    print(params)

    try:
        obj,notif=User.objects.get_or_create(username=params['username'], email=params['email'])
        obj.set_password(params['pass'])
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error", "status":"200"})
    if(notif):
        obj.save()
        obj.first_name=params['fname']
        obj.last_name=params['lname']
        obj.save()

        date = parse_date(params['dob'])

        obj1,notif1=UserDetails.objects.get_or_create(userId=User.objects.get(username=params['username']), address=params['address'], phoneNumber=params['phone'], occupation=params['occupation'], state=params['state'], city=params['city'], country=params['country'], alternatePhoneNumber=params['phone1'], dateOfBirth=date, gender=params['gender'],current_lat=(float)(params['lat']), current_long=(float)(params['long']))
        if(notif1):
            obj1.save()
            obj1.lat_long='POINT('+str(params['lat'])+' '+str(params['long'])+')'
            obj1.profilePhoto=pic
            #obj1.coverPhoto=params['file1']
            obj1.save()
            res=requests.post('https://shielded-dusk-55059.herokuapp.com/user/api/token/', data={'username': params['username'], 'password': params['pass']}).json()
            print(res)
            return JsonResponse({"message":"Success", "status":"201", 'img_url':obj1.profilePhoto.url, 'token_data': res})
        else:
            return JsonResponse({"message":"Error", "status":"203"})


    else:
        return JsonResponse({"message":"Error", "status":"203"})




@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def updateFullUser(request, format=None):
    parser=(MultiPartParser,)
    params=request.data
    pic=request.FILES['photo']
    print(params)
    print(request.user.username)

    currentpassword= request.user.password #user's current password
    user = check_password(params['pass'], currentpassword)
    #user=authenticate(User.objects.get(username=request.user.username).username, params['pass'])
    if(user):
        obj=User.objects.get(username=request.user.username)
        print(params['pass1'])
        obj.set_password(params['pass1'])
        obj.username=params['username']
        obj.first_name=params['fname']
        obj.last_name=params['lname']
        obj.save()
        date = parse_date(params['dob'])
        obj1=UserDetails.objects.get(userId=User.objects.get(username=params['username']))
        obj1.address=params['address']
        obj1.phoneNumber=params['phone']
        obj1.occupation=params['occupation']
        obj1.state=params['state']
        obj1.city=params['city']
        obj1.country=params['country']
        obj1.alternatePhoneNumber=params['phone1']
        obj1.dateOfBirth=date
        obj1.gender=params['gender']
        obj1.current_lat=(float)(params['lat'])
        obj1.current_long=(float)(params['long'])
        obj1.lat_long='POINT('+str(params['lat'])+' '+str(params['long'])+')'
        obj1.profilePhoto=pic
        obj1.save()
        return JsonResponse({"message":"Successfully Updated Profile", "status":"201", 'img_url':obj1.profilePhoto.url})

    else:
        return JsonResponse({"message":"Wrong Password", "status":"404"})


@api_view(['POST'])
@permission_classes((AllowAny, ))
def validateUser(request, format=None):
    params=request.data
    print(params)
    user=authenticate(username=params['username'], password=params['pass'])
    print(user)
    if(user is not None):
        img_url=UserDetails.objects.get(userId=User.objects.get(username=params['username'])).profilePhoto.url
        res=requests.post('https://shielded-dusk-55059.herokuapp.com/user/api/token/', data={'username': params['username'], 'password': params['pass']}).json()
        return JsonResponse({"message": "Success", "status":"200", "img_url":img_url, 'token_data': res})
    else:
        return JsonResponse({"message": "Success", "status":"404"})
