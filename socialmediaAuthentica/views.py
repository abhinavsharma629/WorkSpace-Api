from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from oauth2client.client import OAuth2WebServerFlow
from django.http import JsonResponse
import json
import requests
from pprint import pprint
from oauth2client.file import Storage
from apiclient.discovery import build
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from json import dumps, JSONEncoder, JSONDecoder
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
 # Authorize server-to-server interactions from Google Compute Engine.
import httplib2
from oauth2client.contrib import gce
import base64
import time
from django.urls import reverse
#Using oauth lib for user signing in
from requests_oauthlib import OAuth1Session
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .GoogleDriveTree import googleTree
from .GitHubTree import gitHubTree
from .gitHubNotifications import getGitHubNotifications
from .models import *
import json
from .dropBoxTree import dropBoxTree
from .dropBoxTree1 import dropBoxTree1
from django.core import serializers
from django.db.models import Q
from .userRepo import userRepo, userFollowers, userFollowing
from .models import Trial, CloudOauth2Details
from django.views.decorators.cache import cache_page
from django_user_agents.utils import get_user_agent
from Notifications.models import Notifications
from Notifications.UserAgent import getDeviceDetails

def index(request):
    print(request.user)
    # obj=DataAnalysis.objects.get(user=request.user)
    obj=DataAnalysis.objects.all()
    return render(request, 'socialmediaAuthentication/googleDrivetreeTrail.html', {"obj":obj})

#Folder Hierarchy View
def folderView(request):
    #folderId=request.GET.get('folderId')
    obj1=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName='GOOGLE DRIVE'))
    obj=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName='GOOGLE DRIVE'))
    return render(request, 'socialmediaAuthentication/googleDrivetreeTrail.html', {'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData)})
    #return JsonResponse({'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData)})

def index1(request):
    print(request.user)
    # obj=DataAnalysis.objects.get(user=request.user)
    obj=DataAnalysis.objects.filter(provider=AllAuths.objects.get(authName='DROPBOX'))
    return render(request, 'socialmediaAuthentication/dropBoxTreeTrail.html', {"obj":obj})
    #return JsonResponse({'obj':obj.)})

#Folder Hierarchy View
def folderView1(request):
    #folderId=request.GET.get('folderId')
    obj1=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName='DROPBOX'))
    obj=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName='DROPBOX'))
    return render(request, 'socialmediaAuthentication/dropBoxTreeTrail.html', {'access_token':'Uu-3JJQK28AAAAAAAAABPg_AaJ6lBzbtipyItYT9Q2tC9XWdHJNt6VbEiOGdOEQb', 'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData)})
    #return JsonResponse({'obj':json.dumps(obj.), 'obj1':json.dumps(obj1.hierarchicalData)})




def gitHubfolderView(request):
    #folderId=request.GET.get('folderId')
    #obj1=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName='DROPBOX'))
    obj=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName='GITHUB'))
    return render(request, 'socialmediaAuthentication/gitHubUserProfile.html', {'access_token':'ce688de4b322051ca95aabbad71ceab62867631a', 'obj':json.dumps(obj.rootPageData), 'obj1': obj.rootPageData, 'username': 'abhinavsharma629'})
    #return JsonResponse({'obj':json.dumps(obj.rootPageData)})



def repo(request):
    sha=request.GET.get('sha')
    repoName=request.GET.get('repoName')
    username=request.GET.get('username')
    #Name linked to github account to be saved in db
    url = "https://api.github.com/repos/"+username+"/"+repoName+"/git/trees/"+sha
    querystring = {"recursive":"1"}

    headers = {
        'Authorization': "Bearer ce688de4b322051ca95aabbad71ceab62867631a"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return render(request, 'socialmediaAuthentication/gitHubRepo.html', {'access_token':'ce688de4b322051ca95aabbad71ceab62867631a', 'obj':json.dumps(response), 'sha':sha, 'repoName': repoName, 'username':username})


@cache_page(60 * 15)
def friendList(request):
    if(request.GET.get('username')):
        username=request.GET.get('username')
    else:
        username="abhinavsharma629"
    followers=userFollowers(username)
    print(followers)
    following=userFollowing(username)
    return render(request, 'socialmediaAuthentication/gitHubFriendList.html', {'access_token':'ce688de4b322051ca95aabbad71ceab62867631a', 'followers':followers['followers'], 'following':following['followingUsers']})





@cache_page(60 * 5)
def friendRepos(request, username):
    userRepos=userRepo(username)[0]
    return render(request, 'socialmediaAuthentication/gitHubUserProfile.html', {'access_token':'ce688de4b322051ca95aabbad71ceab62867631a','username':username, 'obj1':userRepos})

@cache_page(60 * 5)
def compareProfiles(request):

    if(len(Trial.objects.filter(username=request.GET.get('username')))==1):
            obj1=Trial.objects.get(username=request.GET.get('username'))
            userRepos=obj1.userRepos
            friend_img_url=obj1.url
            analysisDict=obj1.analysisDict
    else:
            url1="https://api.github.com/users/"+request.GET.get('username')
            userRepos=userRepo(request.GET.get('username'))
            analysisDict=userRepos[1]
            userRepos=userRepos[0]
            friend_img_url=requests.request("GET", url1).json()['avatar_url']
            obj1=Trial(username=request.GET.get('username'), userRepos=userRepos, url=friend_img_url, analysisDict=analysisDict)
            obj1.save()

    url="https://api.github.com/users/abhinavsharma629"
    obj=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName='GITHUB'))
    obj2=DataAnalysis.objects.get(user=User.objects.get(username="abhinavsharma629@gmail.com"), classificationOfDataStorageType="ANALYSIS DATA", provider=AllAuths.objects.get(authName='GITHUB'))
    your_img_url=requests.request("GET", url).json()['avatar_url']

    return render(request, 'socialmediaAuthentication/gitHubComparison.html', {'analysisDict': json.dumps(analysisDict),'access_token':'ce688de4b322051ca95aabbad71ceab62867631a','username':request.GET.get('username'), 'obj1':json.dumps(userRepos), 'obj': json.dumps(obj.rootPageData),'ownerAnalysis': json.dumps(obj2.analysisData), 'yourImg':your_img_url, 'friendImg':friend_img_url})


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def compareUserProfiles(request):
    params=request.GET
    print(params['owner_name'])
    url="https://api.github.com/users/"+params['owner_name']
    url1="https://api.github.com/users/"+params['comparing_user']
    userRepos=userRepo(params['owner_name'], params['access_token'])
    analysisDict=userRepos[1]
    userRepos=userRepos[0]

    userRepos1=userRepo(params['comparing_user'], params['access_token'])
    analysisDict1=userRepos1[1]
    userRepos1=userRepos1[0]

    img_url=requests.request("GET", url).json()['avatar_url']
    img_url1=requests.request("GET", url1).json()['avatar_url']


    return JsonResponse({
        'img_url':img_url,
        'comparing_img_url':img_url1,
        'analysisDict':json.dumps(analysisDict),
        'analysisDict1':json.dumps(analysisDict1),
        'userRepos':json.dumps(userRepos),
        'userRepos1':json.dumps(userRepos1),
        'status':"200"
    })



def friendRepoDetails(request, username):
    sha=request.GET.get('sha')
    repoName=request.GET.get('repoName')

    url = "https://api.github.com/repos/"+username+"/"+repoName+"/git/trees/"+sha
    headers = {
		'Authorization': "Bearer ce688de4b322051ca95aabbad71ceab62867631a",
		'cache-control': "no-cache"
		}
    querystring = {"recursive":"1"}

    response = requests.request("GET", url, params=querystring, headers=headers).json()
    print(response)
    return render(request, 'socialmediaAuthentication/gitHubRepo.html', {'access_token':"ce688de4b322051ca95aabbad71ceab62867631a" ,'username':username, 'obj':json.dumps(response), 'sha':sha, 'repoName': repoName})




def fileDownload(request):
    file_id = request.GET.get('id')
    from googleapiclient.discovery import build
    # credentials=google.oauth2.credentials.Credentials(
    #     access_token= "ya29.Gls7B59OSnp0WGjmDamRyPdmVvquhrsHAnVtrYVxe2ZzwZ3lbOZLnkaga4hqTSafnd1-gMqzGNqDVOnpECEYV5EyVyCiXqKSaa8C7EzH-BnNlqlqgtRBbp6RXU4Y",
    #     refresh_token= "1/MtH9MNG12ApAj_PtnffX6vQnCLBSjH0n1yh2Dha4j_fjiVHYzTQ-VO7GvpRAvAfu",
    #     token_uri = 'https://accounts.google.com/o/oauth2/token',
    #     client_id= "484263106620-gqflub2lb8d0bvbof404133q236utfkn.apps.googleusercontent.com",
    #     client_secret= "7dRw6vDma4uEraS7X7xWT_7z"
    #     )

    credentials=google.oauth2.credentials.Credentials(
        client_id= "484263106620-gqflub2lb8d0bvbof404133q236utfkn.apps.googleusercontent.com",
        token_uri= "https://oauth2.googleapis.com/token",
        client_secret= "7dRw6vDma4uEraS7X7xWT_7z",
        token= "ya29.Gls7B7U9DIGhVdFrXUuD9CCJ46AdGS0PZAn3aBwXDDxQDx8idMxopCR__pmlBvp6N7wJzqjr0GGP0PeNW9x-nm6mXaUCOyjX9RNcJ6gAXVLtGdh3R9yeKnsS957J")
    #authed_session = AuthorizedSession(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v3', http=http)
#     v3 = build('drive', 'v3', credentials={
#         "client_id": "484263106620-gqflub2lb8d0bvbof404133q236utfkn.apps.googleusercontent.com",
#         "project_id": "civic-bruin-237716",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_secret": "7dRw6vDma4uEraS7X7xWT_7z",
#         "redirect_uris": [
#             "http://127.0.0.1:8000/hi/complete/google-oauth2/"
#         ]
# })
    request = v3.files().export_media(fileId=file_id,
                                             mimeType='application/pdf')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    return HttpResponse('of')
#GOOGLE
flow = OAuth2WebServerFlow(client_id='484263106620-gqflub2lb8d0bvbof404133q236utfkn.apps.googleusercontent.com',
                            client_secret='7dRw6vDma4uEraS7X7xWT_7z',
                            scope=['https://www.googleapis.com/auth/plus.login', 'openid',
                            'https://www.googleapis.com/auth/userinfo.email',
                            'https://www.googleapis.com/auth/drive.readonly',
                            'https://www.googleapis.com/auth/drive.metadata',
                            'https://www.googleapis.com/auth/drive.readonly',
                            'https://www.googleapis.com/auth/drive.scripts',
                            'https://www.googleapis.com/auth/drive.photos.readonly',
                            'https://www.googleapis.com/auth/drive.file',
                            'https://www.googleapis.com/auth/drive.appdata'
                            ],

                            redirect_uri='http://127.0.0.1:8000/hi/complete/google-oauth2/')

def login(request):
    auth_uri = flow.step1_get_authorize_url()
    return HttpResponseRedirect(auth_uri)



def complete(request):

    code=request.GET.get('code')
    credentials = flow.step2_exchange(code)
    cred=vars(credentials)
    mainDict={}
    mainDict['id_token']=cred['id_token']
    mainDict['token_response']=cred['token_response']

    outfile=open('createAGoogleDrive.json', 'w')

    dump=json.dumps(vars(credentials), cls=PythonObjectEncoder)
    outfile.write(dump)
    outfile.close()

    headers={}
    headers['Authorization']= 'Bearer '+cred['access_token']
    userDetailsFromToken=requests.get('https://oauth2.googleapis.com/tokeninfo?id_token='+cred['id_token_jwt'], headers=headers)
    userData=userDetailsFromToken.json()

    userDetails=open('googleUserDetails.json', 'w')
    dump=json.dumps(userData)
    userDetails.write(dump)
    userEmail=userData['email']
    print(userEmail)
    # try:
    #     obj=User.objects.get(email=userEmail)
    #     from django.contrib.auth import authenticate
    #     try:
    #         user = authenticate(username=obj.username, password=obj.password)
    #         print('user is:',user)
    #         print(obj.password)
    #         username=obj.username
    #     except Exception as e:
    #         print("Exception" ,e)
    # except Exception as e:
    #     obj,notif=User.objects.get_or_create(username=userData['email'], email=userData['email'])

    #     if(notif):
    #         obj.save()
    #         obj=User.objects.get(username=userData['email'])
    #         obj.set_password='123'
    #         obj.save()

        # user = authenticate(username=userData['email'], password=obj.password)
        # username=userData['email']
        # print(user)

    # googleTree((vars(credentials)['access_token']), request.user.username)
    googleTree((vars(credentials)['access_token']), userEmail)

    #Api
    obj1=DataAnalysis.objects.get(user=User.objects.get(username=userEmail), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName='GOOGLE DRIVE'))
    obj=DataAnalysis.objects.get(user=User.objects.get(username=userEmail), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName='GOOGLE DRIVE'))
    cloudObj, notif= CloudOauth2Details.objects.get_or_create(userId=User.objects.get(username=userEmail), authName=AllAuths.objects.get(authName='GOOGLE DRIVE'), revokeTokenUri= cred['revoke_uri'], accessToken= cred['access_token'], refreshToken=cred['refresh_token'] , tokenExpiry= cred['token_expiry'], idTokenJwt=cred['id_token_jwt'], tokenId=cred['id_token'], tokenInfoUri=cred['token_info_uri'], accessData=dump)
    if(notif):
        cloudObj.save()
    #return JsonResponse({'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData), 'gd_access_token':cloudObj.accessToken , 'gd_refresh_token': cloudObj.refreshToken})

    return HttpResponseRedirect('/hi/folderView')

    '''Post request to:-
    Refresh token url:- https://www.googleapis.com/oauth2/v4/token
    Content type:-  application/x-www-form-urlencoded
    #Body :- client_secret
            grant_type
            refresh token
            client_id'''

    '''Response Body:- {
    "access_token": ,
    "expires_in": 3600,
    "scope": ,
    "token_type": "Bearer",
    "id_token":
    }'''

    #To check details of access_token :- https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=
    # Authorization Endpoint :- https://accounts.google.com/o/oauth2/v2/auth


#Segregated Data List With Fist Paginated Data Data return
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def gd_segregates(request):

    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()==0):
        print("building data")
        if(request.GET.get('authName')=="GOOGLE DRIVE"):
            googleTree(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="GOOGLE DRIVE")).accessToken, request.user)

        elif(request.GET.get('authName')=="DROPBOX"):
            dropBoxTree(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX")).accessToken, request.user)

    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()>0):
        obj=DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="SEGREGATED DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))

        segregates=[]
        c=0
        data={}
        for i in obj:
            #print(type(i.segregatedData))
            if(c==0):
                data={
                "name":i.typeOfData,
                "data":i.segregatedData[i.typeOfData][0:20]}

            segregates.append({"id":c,"name":i.typeOfData})
            c+=1

        segregates.append({
            "id":c,
            "name":"Folder View"})

        return JsonResponse({"data":json.dumps(data), "segregates":segregates, "status":"200"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})





#Segregated Data List With Pagination Data return
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def gd_selected_segregates(request):
    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName')), classificationOfDataStorageType="SEGREGATED DATA", typeOfData=request.GET.get("selName")).count()>0):
        obj=DataAnalysis.objects.get(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName')), classificationOfDataStorageType="SEGREGATED DATA", typeOfData=request.GET.get("selName"))

        startIndex=0
        endIndex=20

        if("startIndex" in request.GET):
            startIndex=(int)(request.GET.get("startIndex"))

        endIndex=(int)(startIndex+20)



        return JsonResponse({"data":json.dumps(obj.segregatedData[request.GET.get("selName")][startIndex:endIndex]), "status":"200"})
    else:
        return JsonResponse({"message":"Data Not Built Yet / No Data Present", "status":"404"})






#Segregated Data List With Pagination Data return
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def db_selected_segregates(request):
    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName')), classificationOfDataStorageType="SEGREGATED DATA", typeOfData=request.GET.get("selName")).count()>0):
        obj=DataAnalysis.objects.get(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName')), classificationOfDataStorageType="SEGREGATED DATA", typeOfData=request.GET.get("selName"))

        startIndex=0
        endIndex=20

        if("startIndex" in request.GET):
            startIndex=(int)(request.GET.get("startIndex"))

        endIndex=(int)(startIndex+20)



        return JsonResponse({"data":json.dumps(obj.segregatedData[startIndex:endIndex]), "status":"200"})
    else:
        return JsonResponse({"message":"Data Not Built Yet / No Data Present", "status":"404"})




#Person Overview Data
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def gd_data_overview(request):
    if(CloudOauth2Details.objects.filter(userId=request.user, authName=AllAuths.objects.get(authName="GOOGLE DRIVE")).count()>0):
        obj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="GOOGLE DRIVE"))

        accessData=obj.accessData
        print(type(accessData))
        img_url=accessData['picture']
        creds={
            "access_token":obj.accessToken,
            "img_url":img_url,
            "refresh_token":obj.refreshToken,
            "id_token":obj.idTokenJwt,
            "token_info_uri":obj.tokenInfoUri,
            "login_email":obj.auth_login_name
        }
        return JsonResponse({"creds":json.dumps(creds), "status":"200"})
    else:
        if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName="GOOGLE DRIVE")).count()>0):
            return JsonResponse({"message":"Multiple Login Account Access Attempt", "status":"500"})
        else:
            return JsonResponse({"message":"Error", "status":"404"})




#Person Overview Data
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def db_data_overview(request):
    if(CloudOauth2Details.objects.filter(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX")).count()>0):
        obj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX"))

        accessData=obj.accessData
        print(type(accessData))
        img_url=accessData['user_details']['profile_photo_url']
        creds={
            "access_token":obj.accessToken,
            "img_url":img_url,
            "id_token":obj.idTokenJwt,
            "login_email":accessData['user_details']['email']
        }
        return JsonResponse({"creds":json.dumps(creds), "status":"200"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})



#Segregated Data List With Fist Paginated Data Data return
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def db_segregates(request):

    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()==0):
        print("building data")
        if(request.GET.get('authName')=="DROPBOX"):
            dropBoxTree1(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX")).accessToken, request.user)

    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()>0):
        obj=DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="SEGREGATED DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))

        segregates=[]
        c=0
        data={}
        for i in obj:
            #print(type(i.segregatedData))
            if(c==0):
                data={
                "name":i.typeOfData,
                "data":i.segregatedData[0:20]}

            segregates.append({"id":c,"name":i.typeOfData})
            c+=1

        segregates.append({
            "id":c,
            "name":"Folder View"})

        return JsonResponse({"data":json.dumps(data), "segregates":segregates, "status":"200"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})






#Person Overview Data
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def ma_data_overview(request):
    print(request.GET)
    if(CloudOauth2Details.objects.filter(userId=request.user, authName=AllAuths.objects.get(authName="AZURE")).count()>0):
        obj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="AZURE"))

        accessData=obj.accessData
        print(type(accessData))

        creds={
            "access_token":obj.accessToken,
            "refresh_token":obj.refreshToken,
            "login_email":obj.auth_login_name
        }
        return JsonResponse({"creds":json.dumps(creds), "status":"200"})
    else:
        return JsonResponse({"message":"Error", "status":"404"})










@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def storeCloud(request):
    print("Logged in user is:- ",request.user.username)
    print(request.POST.get('cred'))
    print(type(request.POST.get('cred')))
    print(request.data)
    cred=json.loads(request.data.get('cred'))

    dump=json.loads(request.data.get('dump'))

    userObj=User.objects.get(username=request.user.username)

    # if((CloudOauth2Details.objects.filter( ~Q(userId=userObj), Q(auth_login_name=request.data.get('email')), Q(authName=AllAuths.objects.get(authName=request.data.get('authName')))).count()==1) or (DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()>0)):
    #     obj=CloudOauth2Details.objects.get(auth_login_name=request.data.get('email'), authName=AllAuths.objects.get(authName=request.data.get('authName')))
    #     obj.revokeTokenUri= cred['revoke_uri']
    #     obj.accessToken= cred['access_token']
    #     obj.refreshToken=cred['refresh_token']
    #     obj.tokenExpiry= cred['token_expiry']
    #     obj.idTokenJwt=cred['id_token_jwt']
    #     obj.tokenId=cred['id_token']
    #     obj.tokenInfoUri=cred['token_info_uri']
    #     obj.accessData=dump
    #     obj.save()
    #     # CloudOauth2Details.objects.filter(auth_login_name=request.data.get('email')).delete()
    #     return JsonResponse({"message":"Multiple Login Attempt", "status":"500"})
    # else:
    if(CloudOauth2Details.objects.filter(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName'))).count()==1):
        obj=CloudOauth2Details.objects.get(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName')))
        if(request.data.get('authName')=="GOOGLE DRIVE"):
            obj.authName=AllAuths.objects.get(authName=request.data.get('authName'))
            obj.auth_login_name=request.data.get('email')
            obj.revokeTokenUri= cred['revoke_uri']
            obj.accessToken= cred['access_token']
            obj.refreshToken=cred['refresh_token']
            obj.tokenExpiry= cred['token_expiry']
            obj.idTokenJwt=cred['id_token_jwt']
            obj.tokenId=cred['id_token']
            obj.tokenInfoUri=cred['token_info_uri']
            obj.accessData=dump
            obj.save()
        elif(request.data.get('authName')=="DROPBOX"):
            obj.authName=AllAuths.objects.get(authName=request.data.get('authName'))
            obj.auth_login_name=request.data.get('email')
            obj.accessToken= cred['access_token']
            obj.tokenId=cred['uid']
            obj.accessData=dump
            obj.save()
        elif(request.data.get('authName')=="GITHUB"):
            obj.authName=AllAuths.objects.get(authName=request.data.get('authName'))
            obj.auth_login_name=request.data.get('auth_login_name')
            obj.accessToken= request.data.get('access_token')
            obj.accessData=dump
            obj.save()
        elif(request.data.get('authName')=="AZURE"):
            obj.authName=AllAuths.objects.get(authName=request.data.get('authName'))
            obj.auth_login_name=request.data.get('email')
            obj.accessToken= cred['access_token']
            obj.refreshToken=cred['refresh_token']
            obj.accessData=dump
            obj.save()

        return JsonResponse({"message": "Already Exists", "status": "203"})
    else:
        if(request.data.get('authName')=="GOOGLE DRIVE"):
            cloudObj, notif= CloudOauth2Details.objects.get_or_create(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName')), auth_login_name=request.data.get('email'), revokeTokenUri= cred['revoke_uri'], accessToken= cred['access_token'], refreshToken=cred['refresh_token'] , tokenExpiry= cred['token_expiry'], idTokenJwt=cred['id_token_jwt'], tokenId=cred['id_token'], tokenInfoUri=cred['token_info_uri'], accessData=dump)

        elif(request.data.get('authName')=="DROPBOX"):
            cloudObj, notif= CloudOauth2Details.objects.get_or_create(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName')), auth_login_name=request.data.get('email'), accessToken= cred['access_token'] , tokenId=cred['uid'], accessData=dump)

        elif(request.data.get('authName')=="GITHUB"):
            cloudObj, notif= CloudOauth2Details.objects.get_or_create(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName')),auth_login_name=request.data.get('auth_login_name'), accessToken= request.data.get('access_token') , accessData=dump)

        elif(request.data.get('authName')=="AZURE"):
            cloudObj, notif= CloudOauth2Details.objects.get_or_create(userId=userObj, authName=AllAuths.objects.get(authName=request.data.get('authName')),auth_login_name=request.data.get('email'), accessToken= request.data.get('access_token') , accessData=dump, refreshToken=request.data.get('refresh_token'))

        if(notif):
            cloudObj.save()
        return JsonResponse({"message": "Created", "status": "201"})




#Specifically For Checking And Building Drive Data
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def buildDriveForDrive(request):
    print(request.user)
    print(request.GET.get('authName'))
    if(CloudOauth2Details.objects.filter(userId=request.user).count()==0):
        return JsonResponse({"message":"Multiple Account Login Attempt", "status":"400"})
    else:
        if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()==0):
            if(request.GET.get('authName')=="GOOGLE DRIVE"):
                googleTree(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="GOOGLE DRIVE")).accessToken, request.user.username)
                return JsonResponse({"message":"Successfully Built Drive Data", "status":"200"})
            else:
                return JsonResponse({"message":"Not Supported Cloud", "status":"500"})
        else:
            return JsonResponse({"message":"Already Built Drive Data", "status":"200"})


#Specifically For Checking And Building Drive Data
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def buildDropboxForDropbox(request):
    print(request.user)
    print(request.GET.get('authName'))
    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()==0):
        if(request.GET.get('authName')=="DROPBOX"):
            dropBoxTree1(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX")).accessToken, request.user)
            return JsonResponse({"message":"Successfully Built Dropbox Data", "status":"200"})
        else:
            return JsonResponse({"message":"Not Supported Cloud", "status":"500"})
    else:
        return JsonResponse({"message":"Already Built Dropbox Data", "status":"200"})


#Specifically For rootPageData For Drive
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def rootFolderDataForDrive(request):
    if(DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName="GOOGLE DRIVE")).count()>0):

        obj=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName="GOOGLE DRIVE")).rootPageData
        return JsonResponse({'message':'success', 'rootData':json.dumps(obj), 'status':'200'})
    else:
        return JsonResponse({'message':'Drive Not Built', 'status':'404'})


#Specifically For rootPageData For Drive
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def rootFolderDataForDropbox(request):
    if(DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName="DROPBOX")).count()>0):

        obj=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName="DROPBOX")).rootPageData
        return JsonResponse({'message':'success', 'rootData':json.dumps(obj), 'status':'200'})
    else:
        return JsonResponse({'message':'Drive Not Built', 'status':'404'})




#Specifically For hierarchicalData For Drive With Pagination
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def hierarchicalFolderDataForDrive(request):
    startIndex=0
    endIndex=20

    if('startIndex' in request.GET):
        startIndex=request.GET.get("startIndex")
    if('endIndex' in request.GET):
        endIndex=request.GET.get("endIndex")
    else:
        endIndex=startIndex+20


    if(DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="HIERARCHICAL DATA",provider=AllAuths.objects.get(authName="GOOGLE DRIVE")).count()>0):

        obj=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="HIERARCHICAL DATA",provider=AllAuths.objects.get(authName="GOOGLE DRIVE")).hierarchicalData
        if(request.GET.get('currentAccessId') in obj):
            children=[]
            currentChild={}
            children=obj[request.GET.get('currentAccessId')]['children']
            print(children)
            print(startIndex, endIndex)
            children=children[(int)(startIndex):(int)(endIndex)]
            for i in children:
                print(i)
                print(obj[i])
                currentChild[i]=obj[i]

            print(currentChild)
            return JsonResponse({'message':'success', 'hierarchicalData':json.dumps(currentChild), 'status':'200'})
        else:
            return JsonResponse({'message':'Id Not Found', 'status':'404'})

    else:
        return JsonResponse({'message':'Drive Not Built', 'status':'404'})


#Specifically For hierarchicalData For Drive With Pagination
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def hierarchicalFolderDataForDropbox(request):
    startIndex=0
    endIndex=20

    if('startIndex' in request.GET):
        startIndex=request.GET.get("startIndex")
    if('endIndex' in request.GET):
        endIndex=request.GET.get("endIndex")
    else:
        endIndex=startIndex+20


    if(DataAnalysis.objects.filter(user=request.user, classificationOfDataStorageType="HIERARCHICAL DATA",provider=AllAuths.objects.get(authName="DROPBOX")).count()>0):
        print(request.GET.get('currentAccessId')+"/")
        obj=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="HIERARCHICAL DATA",provider=AllAuths.objects.get(authName="DROPBOX")).hierarchicalData
        if(request.GET.get('currentAccessId')+"/" in obj):
            children=[]
            currentChild={}
            children=obj[request.GET.get('currentAccessId')+"/"]['children']
            print(children)
            print(startIndex, endIndex)
            children=children[(int)(startIndex):(int)(endIndex)]
            # for i in children:
            #     print(i)
            #     print(obj[i])
            #     currentChild[i]=obj[i]

            print(currentChild)
            return JsonResponse({'message':'success', 'hierarchicalData':json.dumps(children), 'status':'200'})
        else:
            return JsonResponse({'message':'Id Not Found', 'status':'404'})

    else:
        return JsonResponse({'message':'Drive Not Built', 'status':'404'})



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def buildDrive(request):
    print(request.user)
    print(request.GET.get('authName'))
    if(DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.GET.get('authName'))).count()==0):
        if(request.GET.get('authName')=="GOOGLE DRIVE"):
            googleTree(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="GOOGLE DRIVE")).accessToken, request.user)

        elif(request.GET.get('authName')=="DROPBOX"):
            dropBoxTree(CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="DROPBOX")).accessToken, request.user)


        elif(request.GET.get('authName')=="GITHUB"):
            obj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName="GITHUB"))
            gitHubTree(obj.accessToken, request.user, obj.auth_login_name)
            obj1=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ANALYSIS DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            obj=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            cloudObj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName')))

            return JsonResponse({'RootFolder':json.dumps(obj.rootPageData), 'AnalysisData':json.dumps(obj1.analysisData), 'access_token':cloudObj.accessToken , 'refresh_token': cloudObj.refreshToken})

        #Api
        obj1=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
        obj=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
        cloudObj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName')))

        return JsonResponse({'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData), 'access_token':cloudObj.accessToken , 'refresh_token': cloudObj.refreshToken})

    else:
        if(request.GET.get('authName')!="GITHUB"):
            obj1=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            obj=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            cloudObj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName')))

            return JsonResponse({'obj':json.dumps(obj.rootPageData), 'obj1':json.dumps(obj1.hierarchicalData), 'access_token':cloudObj.accessToken , 'refresh_token': cloudObj.refreshToken})
        else:
            obj1=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ANALYSIS DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            obj=DataAnalysis.objects.get(user=User.objects.get(username=request.user), classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName=request.GET.get('authName')))
            cloudObj=CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName')))

            return JsonResponse({'RootFolder':json.dumps(obj.rootPageData), 'AnalysisData':json.dumps(obj1.analysisData), 'access_token':cloudObj.accessToken , 'refresh_token': cloudObj.refreshToken})



@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
def socialLogout(request):
    try:
        CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.data['authName'])).delete()
        DataAnalysis.objects.filter(user=request.user, provider=AllAuths.objects.get(authName=request.data['authName'])).delete()
        return JsonResponse({'message': "Deleted", "status":"200"})
    except Exception as e:
        return JsonResponse({'message': "Error", "status":"400"})



#GITHUB
def gitHubLogin(request):
    return HttpResponseRedirect("https://github.com/login/oauth/authorize?client_id=62214c9c431303a8217c&client_secret=2513fa09a6a01b3956bc1ace331d0c9325fa2b7e&scope=notifications,user,repo:status,read:user,repo,delete_repo,email")

def gitHubComplete(request):
    print(request.GET)
    code=request.GET.get('code')
    print("Code is:- ",code)
    data={
        'client_id':'62214c9c431303a8217c',
        'client_secret':"2513fa09a6a01b3956bc1ace331d0c9325fa2b7e",
        'state':'notifications,user,email,repo',
        'code':code,
        'redirect_uri':"http://127.0.0.1:8000/hi/complete/gitHub-oauth2"
        }
    headers={}
    headers['Accept']="application/json"
    accessTokenData=requests.post("https://github.com/login/oauth/access_token", data=data, headers=headers)
    #print(accessTokenData.text)
    accessTokenDataToJson=json.loads(accessTokenData.text)
    header={}
    try:
        header['Authorization']="Bearer "+accessTokenDataToJson['access_token']
    except:
        return HttpResponseRedirect('/hi/gitHubLogin')
    userDetails=requests.get("https://api.github.com/user", headers=header)
    #print(userDetails)
    userDetailsToJson=json.loads(userDetails.text)

    url = "https://api.github.com/user/emails"

    headers = {
        'Authorization': "Bearer "+str(accessTokenDataToJson['access_token']),
        'Host': "api.github.com"
        }

    response = requests.request("GET", url, headers=headers)

    userDetailsToJson['email']=response.json()[0]

    concatinatingTheTwoJsonObjects={}
    concatinatingTheTwoJsonObjects['user_details']=userDetailsToJson
    concatinatingTheTwoJsonObjects['token_details']=accessTokenDataToJson

    gitHubCred=open('gitHubCred.json' , 'w')
    json.dump(concatinatingTheTwoJsonObjects, gitHubCred, indent=4)
    gitHubCred.close()


    gitHubTree(userDetailsToJson['email']['email'],userDetailsToJson['login'], accessTokenDataToJson['access_token'])

    return HttpResponseRedirect('/hi/gitHubfolderView')

def getGitHubNotifications(request):
    getGitHubNotifications(request.user, access_token)

'''Have to create own encoder for encoding obj types like list, dict, set, datetime obj
    For list, dict -> JSONEncoder encodes into json
    set -> return a list as list is json serializable
    datetime -> we have an invuilt DjangoJSONEncoder for serializing datetime obj'''


#JSON OBJECTS ENCODER
class PythonObjectEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, (datetime.date, datetime.datetime)):
                return DjangoJSONEncoder.default(self, obj)





#REDDIT
def redditLogin(request):
    return HttpResponseRedirect("https://www.reddit.com/api/v1/authorize?client_id=G_q8PjRtFpua0w&response_type=code&state=stae123abc&duration=permanent&redirect_uri=http://127.0.0.1:8000/hi/complete/reddit-oauth2&duration=permanent&scope=identity,edit,flair,history,modconfig,modflair,modlog,modposts,modwiki,mysubreddits,privatemessages,read,report,save,submit,subscribe,vote,wikiedit,wikiread")

def redditComplete(request):
    print("Request is:- ",request.GET)
    code=request.GET.get('code')
    print("Code is:- ", code)
    headers={}
    url = "https://www.reddit.com/api/v1/access_token"

    payload = "grant_type=authorization_code&code="+str(code)+"&redirect_uri=http://127.0.0.1:8000/hi/complete/reddit-oauth2"
    # headers = {
    #     'Content-Type': "application/x-www-form-urlencoded",
    #     'Authorization': "Basic "+(base64.b64encode(b"G_q8PjRtFpua0w:V3sRErXzcFovUB1iEwW30oaoR9w").decode("utf-8")),
    #     'Cache-Control': "no-cache",
    #     'cache-control': "no-cache"
    #     }

    headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Basic R19xOFBqUnRGcHVhMHc6VjNzUkVyWHpjRm92VUIxaUV3VzMwb2FvUjl3",
    'User-Agent': "PostmanRuntime/7.13.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "www.reddit.com"
    }

    tokenData = requests.request("POST", url, data=payload, headers=headers)

    #print(response.text)
    tokenDataToJson=json.loads(tokenData.text)
    print("Json Data:- ",tokenDataToJson)



    redditToken=open('redditCred.json', 'w')
    # header = {
    #         'Authorization': "Bearer "+,
    #         }
    headers = {
    'Authorization': "Bearer "+tokenDataToJson['access_token'],
    'User-Agent': "PostmanRuntime/7.13.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "500e004a-d5a6-49f9-a8ec-fa5c47cb456d,100f3131-82c6-4874-89d1-57450c75c5b6",
    'Host': "oauth.reddit.com",
    'cookie': "loid=00000000003vqdb0vi.2.1559561520865.Z0FBQUFBQmM5UVV3T2hON0RDckthNk1Id3liQ3dJOXozV2kyUUFrTmduOHhMamxYMUd6VEZDQ3pIb2ZBSy1sZDhhRjU0cFYyLWNXYU56SWk1d1ZtQXZDT29rSWxnSWVKdDJlbWU4ZURxY3c3LVR3VzJjcmpsM2F2azFfX2lVdDM2czNZSjF5MDkzb3Q; edgebucket=j3viGiyoo6cRbf0INs",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
    print(headers)
    redditUserDetails=requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    print(redditUserDetails)
    redditUserCreds={}
    redditUserCreds['token_details']=tokenDataToJson
    redditUserCreds['user_details']=json.loads(redditUserDetails.text)
    json.dump(redditUserCreds, redditToken)
    redditToken.close()
    return HttpResponse("<code>"+str(redditUserCreds)+"</code>")

    # except Exception as e:
    #     return HttpResponse("<pre>Some Error Occured With the OAuth</pre><br><pre>In particular with "+str(e)+"</pre>")



    ''' The refresh token here is permanent
    To Refresh The Token In reddit:-

    url = "https://www.reddit.com/api/v1/access_token"

    payload = "grant_type=refresh_token&refresh_token=refreshToken"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Basic R19xOFBqUnRGcHVhMHc6VjNzUkVyWHpjRm92VUIxaUV3VzMwb2FvUjl3",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    '''




#TWITTER Still uses OAuth1
global resourceOwnerAuthTokenDetails
resourceOwnerAuthTokenDetails=[]
def twitterLogin(request):
    # url = "https://api.twitter.com/oauth2/token"
    # data={
    #     "Content-Type":"application/x-www-form-urlencoded",
    #     "grant_type":"client_credentials",
    #     "Content-Length":"29",
    #     "User-Agent":"My Twitter App v1.0.23",
    #     "Accept-Encoding":"gzip"
    # }

    # headers={
    #     'Authorization': "Basic RVlXb25KUEhBcU1PR3htZE85cHB3QXZQTDowRmF6RkZVRFUzMzl3Z2pXUllTWHZkRVUzMzFvWG5iRGdtYnVQUlFIeDBpVlFrS09ZSw=="
    #     }

    # response = requests.post(url, data=data, headers=headers)

    # print(response.text)
    # auth_token=json.loads(response.text)['access_token']

    headers={
        'Authorization': "OAuth oauth_consumer_key=EYWonJPHAqMOGxmdO9ppwAvPL,oauth_token=601124230-KX7zxOMb3dpa5I1G5bAncevBeLIv0s5IDHd3o33H,oauth_signature_method=HMAC-SHA1,oauth_timestamp=1559587695,oauth_nonce=abcdMh7hUSH,oauth_version=1.0,oauth_signature=AKkkG14fGt1lLFQ4GEHurpNSOAg%3D"
    }
    requestAuthToken=requests.post('https://api.twitter.com/oauth/request_token', headers=headers)
    print(requestAuthToken.text)
    requestAuthToken=str(requestAuthToken.text).split('&')
    authToken=(requestAuthToken[0])[12:]
    print(authToken)
    print(requestAuthToken[1][19:])

    resourceOwnerAuthTokenDetails.append(authToken)
    resourceOwnerAuthTokenDetails.append(requestAuthToken[1][19:])
    return HttpResponseRedirect('https://api.twitter.com/oauth/authorize?oauth_token='+authToken)

def twitterComplete(request):
    #Using py oauth lib
    oauth_token = OAuth1Session(client_key='EYWonJPHAqMOGxmdO9ppwAvPL',
                                    client_secret='0FazFFUDU339wgjWRYSXvdEU331oXnbDgmbuPRQHx0iVQkKOYK',
                                    resource_owner_key=request.GET.get('oauth_token'),
                                    resource_owner_secret=resourceOwnerAuthTokenDetails[1])
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_verifier": request.GET.get('oauth_verifier')}
    access_token_data = oauth_token.post(url, data=data)
    print(access_token_data.text)
    oauthConsumerTokenDetails={}
    accessTokenData=(access_token_data.text).split('&')
    authToken={}
    authToken['oauth_token']=accessTokenData[0][12:]
    authToken['oauth_token_secret']=accessTokenData[1][19:]
    oauthConsumerTokenDetails['customerTokenDetails']=authToken
    userId=accessTokenData[2][8:]
    userName=accessTokenData[3][12:]

    #print(userName, userId, authToken)


    # url = "https://api.twitter.com/1.1/account/verify_credentials.json"

    # headers = {
    #     'Authorization': "OAuth oauth_consumer_key=EYWonJPHAqMOGxmdO9ppwAvPL,oauth_token=601124230-KX7zxOMb3dpa5I1G5bAncevBeLIv0s5IDHd3o33H,oauth_signature_method=HMAC-SHA1,oauth_timestamp=1559624331,oauth_nonce=2FMQ1fwQq0J,oauth_version=1.0,oauth_signature=IdlJrO%2Ff6N0p7gqDrCPURMd8XyU%3D",
    #     'User-Agent': "PostmanRuntime/7.13.0",
    #     'Accept': "*/*",
    #     'Cache-Control': "no-cache",
    #     'Postman-Token': "ee70202e-3805-47df-96eb-070ee0daf18c,b39d197d-5679-4dbd-9313-2252b509dd14",
    #     'Host': "api.twitter.com",
    #     'accept-encoding': "gzip, deflate",
    #     'Connection': "keep-alive",
    #     'cache-control': "no-cache"
    #     }

    # params = {
    #     'Name': userName,
    #     'include_entities': "true",
    #     'skip_status': "false",
    #     'include_email': "true"
    #     }
    # userData=oauth_token.get(url, params=params)
    # print(userData.json())


    oauth_user = OAuth1Session(client_key='EYWonJPHAqMOGxmdO9ppwAvPL',
                               client_secret='0FazFFUDU339wgjWRYSXvdEU331oXnbDgmbuPRQHx0iVQkKOYK',
                               resource_owner_key=authToken['oauth_token'],
                               resource_owner_secret=authToken['oauth_token_secret']
                               )
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    params = {
        'Name': userName,
        'include_entities': "true",
        'skip_status': "false",
        'include_email': "true"
        }
    user_data = oauth_user.get(url_user, params=params)
    print(user_data.json())

    oauthConsumerTokenDetails['userDetails']=user_data.json()

    twitterCredData=open('twitterUserCred.json', 'w')
    json.dump(oauthConsumerTokenDetails, twitterCredData)
    twitterCredData.close()

    return HttpResponse("<h1><pre>Ok Done</pre><br><pre>"+access_token_data.text+"</pre></h1>")




#FACEBOOK
def fbLogin(request):
    return HttpResponseRedirect('/hi/complete/facebook-oauth2')

def fbComplete(request):
    return HttpResponse('Ok Done')






#DROPBOX
def dropboxLogin(request):
    clientId="0g2qw3uaxpgwbsf"
    #url="https://www.dropbox.com/oauth2/authorize?client_id="+clientId+"&response_type=code&redirect_uri=http:127.0.0.1:8000/hi/complete/dropbox-oauth2"

    url="https://www.dropbox.com/oauth2/authorize?client_id="+clientId+"&response_type=code&redirect_uri=http://127.0.0.1:8000/hi/complete/dropbox-oauth2"
    # response=requests.get(url)
    # print(response)
    return HttpResponseRedirect(url)

def dropboxComplete(request):
    # from django.template import RequestContext
    # print(RequestContext(request)) #Get Request context
    code=request.GET.get('code')

    print(code)
    url = "https://api.dropboxapi.com/oauth2/token"

    payload1 = "code="+str(code)+"&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/hi/complete/dropbox-oauth2"
    headers1 = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Basic MGcycXczdWF4cGd3YnNmOnl4dHhhMWg0YWU0cDhmMw==",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "api.dropboxapi.com",
        'accept-encoding': "gzip, deflate",
        'content-length': "154",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload1, headers=headers1)

    response=response.json()
    print(response)
    try:
        accessToken=response['access_token']
    except Exception as e:
        return HttpResponseRedirect('/hi/dropboxLogin')

    print(accessToken)
    uid=response['uid']
    print(uid)
    accountId=response['account_id']
    print(accountId)
    url = "https://api.dropboxapi.com/2/users/get_current_account"

    headers = {
            'Authorization': "Bearer "+str(accessToken)
        }

    response1 = requests.request("POST", url, headers=headers)
    print(response1.json())
    dropBoxDetails={}
    dropBoxCred={}
    dropBoxCred['access_token']=accessToken
    dropBoxCred['uid']=uid
    dropBoxCred['account_id']=accountId
    dropBoxDetails['credentials']=dropBoxCred
    dropBoxDetails['user_details']=response1.json()
    dropBoxFile=open('dropBoxUserDetails.json', 'w')
    json.dump(dropBoxDetails, dropBoxFile)
    dropBoxFile.close()

    email=response1.json()['email']
    dropBoxTree(accessToken, email)
    return HttpResponse("Ok Done")
    # except Exception as e:
    #     return HttpResponse(str(e))
    # # curl -X POST https://api.dropboxapi.com/2/auth/token/revoke \
    #--header "Authorization: Bearer "  --> Used to disable tokens used for api calls



#ONE DRIVE
def oneDriveLogin(request):
    url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
    params={
        'client_id':'0831a781-a072-4bc2-9294-fd79b4ca082e',
        'scope':'onedrive.readwrite, wl.offline_access',
        'response_type':'code',
        'redirect_uri':'https://shielded-dusk-55059.herokuapp.com/hi/complete/oneDrive-oauth21'
    }

    import urllib.parse
    #Making the query url
    urlParam=urllib.parse.urlencode(params)
    print(urlParam)
    return HttpResponseRedirect(str(url+urlParam))

def oneDriveComplete(request):
    ONEDRIVE_CLIENT_SECRET="tjrgDSA!qkpSPYI25943%7B%5D%3F"
    ONEDRIVE_CLIENT_ID="0831a781-a072-4bc2-9294-fd79b4ca082e"
    ONEDRIVE_REDIRECT_URI="http://127.0.0.1:8000/hi/complete/oneDrive-oauth2"

    print("GET:- ",request.GET)
    code=request.GET.get('code')

    print(code)
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = "client_id="+ONEDRIVE_CLIENT_ID+"&redirect_uri="+ONEDRIVE_REDIRECT_URI+"&client_secret="+ONEDRIVE_CLIENT_SECRET+"&code="+str(code)+"&grant_type=authorization_code&scope=user.read"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "login.microsoftonline.com",
        'cookie': "buid=AQABAAEAAADCoMpjJXrxTq9VG9te-7FXdF5conme6fNqjdiRBKElK6DOuE7g9rxbHk0J4cVfkhyDO94HIPBECOFSvIoniBPgXMFOPKmc6vAZJZZ8kvnkB1Lk54k7otPLp7BwvC6yqmcgAA; fpc=AmELew3xLfpMjD-FzTvNlRhtMOofAQAAAAmTmNQOAAAA; esctx=AQABAAAAAADCoMpjJXrxTq9VG9te-7FXw1EQWCa_qpBHd2IohA8PgBO6R_pz5zRjF0gYb_E_Q86jvXRWZP6dpPVX94u-GgCYeja702gmW-tYiQCiNE9uXSJ9qR_DhJjXzM_Sxj953w97bQBQ2AebN5LVPrEtWeE7jGVRC19QR1EI7-vK70pvdcP7Ugbxo45ZrxQdfMK_E3IgAA; x-ms-gateway-slice=prod; stsservicecookie=ests",
        'accept-encoding': "gzip, deflate",
        'content-length': "242",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    oneDrive=open('oneDriveUserDetails.json', 'w')
    userCred={}
    userCred['token_details']=response.json()

    print(json.dumps(response.json(), indent=2))

    userDataUrl="https://graph.microsoft.com/v1.0/me"
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+response.json()['access_token'],
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "graph.microsoft.com",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

    response1 = requests.request("GET", userDataUrl, headers=headers)
    userCred['user_details']=response1.json()

    json.dump(userCred, oneDrive)
    oneDrive.close()
    return HttpResponse("OneDrive Done")

    '''GET NEW ACCESS && REFRESH TOKEN

    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    payload = "client_id="+ONEDRIVE_CLIENT_ID+"&redirect_uri="+ONEDRIVE_REDIRECT_URI+"&client_secret="+ONEDRIVE_CLIENT_SECRET+"&code="+str(code)+"&grant_type=refresh_token&refresh_token=PREVIOUS_REFRESH_TOKEN"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "login.microsoftonline.com",
        'cookie': "buid=AQABAAEAAADCoMpjJXrxTq9VG9te-7FXdF5conme6fNqjdiRBKElK6DOuE7g9rxbHk0J4cVfkhyDO94HIPBECOFSvIoniBPgXMFOPKmc6vAZJZZ8kvnkB1Lk54k7otPLp7BwvC6yqmcgAA; fpc=AmELew3xLfpMjD-FzTvNlRhtMOofAQAAAAmTmNQOAAAA; esctx=AQABAAAAAADCoMpjJXrxTq9VG9te-7FXw1EQWCa_qpBHd2IohA8PgBO6R_pz5zRjF0gYb_E_Q86jvXRWZP6dpPVX94u-GgCYeja702gmW-tYiQCiNE9uXSJ9qR_DhJjXzM_Sxj953w97bQBQ2AebN5LVPrEtWeE7jGVRC19QR1EI7-vK70pvdcP7Ugbxo45ZrxQdfMK_E3IgAA; x-ms-gateway-slice=prod; stsservicecookie=ests",
        'accept-encoding': "gzip, deflate",
        'content-length': "242",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    '''





def oneDriveComplete1(request):
    ONEDRIVE_CLIENT_SECRET="tjrgDSA!qkpSPYI25943%7B%5D%3F"
    ONEDRIVE_CLIENT_ID="0831a781-a072-4bc2-9294-fd79b4ca082e"
    ONEDRIVE_REDIRECT_URI="https://shielded-dusk-55059.herokuapp.com/hi/complete/oneDrive-oauth21"

    print("GET:- ",request.GET)
    code=request.GET.get('code')
    state=request.GET.get('state')
    print(state)

    print(code)
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    payload = "client_id="+ONEDRIVE_CLIENT_ID+"&redirect_uri="+ONEDRIVE_REDIRECT_URI+"&client_secret="+ONEDRIVE_CLIENT_SECRET+"&code="+str(code)+"&grant_type=authorization_code&scope=user.read"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "login.microsoftonline.com",
        'cookie': "buid=AQABAAEAAADCoMpjJXrxTq9VG9te-7FXdF5conme6fNqjdiRBKElK6DOuE7g9rxbHk0J4cVfkhyDO94HIPBECOFSvIoniBPgXMFOPKmc6vAZJZZ8kvnkB1Lk54k7otPLp7BwvC6yqmcgAA; fpc=AmELew3xLfpMjD-FzTvNlRhtMOofAQAAAAmTmNQOAAAA; esctx=AQABAAAAAADCoMpjJXrxTq9VG9te-7FXw1EQWCa_qpBHd2IohA8PgBO6R_pz5zRjF0gYb_E_Q86jvXRWZP6dpPVX94u-GgCYeja702gmW-tYiQCiNE9uXSJ9qR_DhJjXzM_Sxj953w97bQBQ2AebN5LVPrEtWeE7jGVRC19QR1EI7-vK70pvdcP7Ugbxo45ZrxQdfMK_E3IgAA; x-ms-gateway-slice=prod; stsservicecookie=ests",
        'accept-encoding': "gzip, deflate",
        'content-length': "242",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    #oneDrive=open('oneDriveUserDetails.json', 'w')
    userCred={}
    userCred['token_details']=response.json()

    #print(json.dumps(response.json(), indent=2))

    userDataUrl="https://graph.microsoft.com/v1.0/me"
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer "+response.json()['access_token'],
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "graph.microsoft.com",
    'accept-encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

    response1 = requests.request("GET", userDataUrl, headers=headers)
    userCred['user_details']=response1.json()
    print(json.dumps(userCred, indent=4))

    #json.dump(userCred, oneDrive)
    #oneDrive.close()
    #return HttpResponse("OneDrive Done")
    headers1={}
    headers1['Authorization']= 'Bearer '+request.GET.get('state')
    url="https://shielded-dusk-55059.herokuapp.com/hi/storeCloud"

    response=requests.post(url, data={
        'access_token':userCred['token_details']['access_token'],
        'refresh_token':userCred['token_details']['refresh_token'],
        'email':userCred['user_details']['userPrincipalName'],
        'cred':json.dumps(userCred),
        'dump':json.dumps(userCred),
        'authName': "AZURE"
    }, headers=headers1).json()

    print(response)

    if(response['status']=='201'):
        result="A Duplicate User With the Email Of Registered Drive Already Exists in our Database!! Please try again with that account (if its yours) or report an issue if you notice something unusual!!"
    else:
        result="Your Drive Data Will Soon Be Loaded!! We are analysing it!! Be Patient!!"
    return JsonResponse({"message":"Successfully Saved", "status":"201"})

    #return JsonResponse({'message':"Successfully Saved", "status":"200"})
    '''GET NEW ACCESS && REFRESH TOKEN

    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    payload = "client_id="+ONEDRIVE_CLIENT_ID+"&redirect_uri="+ONEDRIVE_REDIRECT_URI+"&client_secret="+ONEDRIVE_CLIENT_SECRET+"&code="+str(code)+"&grant_type=refresh_token&refresh_token=PREVIOUS_REFRESH_TOKEN"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "login.microsoftonline.com",
        'cookie': "buid=AQABAAEAAADCoMpjJXrxTq9VG9te-7FXdF5conme6fNqjdiRBKElK6DOuE7g9rxbHk0J4cVfkhyDO94HIPBECOFSvIoniBPgXMFOPKmc6vAZJZZ8kvnkB1Lk54k7otPLp7BwvC6yqmcgAA; fpc=AmELew3xLfpMjD-FzTvNlRhtMOofAQAAAAmTmNQOAAAA; esctx=AQABAAAAAADCoMpjJXrxTq9VG9te-7FXw1EQWCa_qpBHd2IohA8PgBO6R_pz5zRjF0gYb_E_Q86jvXRWZP6dpPVX94u-GgCYeja702gmW-tYiQCiNE9uXSJ9qR_DhJjXzM_Sxj953w97bQBQ2AebN5LVPrEtWeE7jGVRC19QR1EI7-vK70pvdcP7Ugbxo45ZrxQdfMK_E3IgAA; x-ms-gateway-slice=prod; stsservicecookie=ests",
        'accept-encoding': "gzip, deflate",
        'content-length': "242",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    '''



#PUT CLOUD DATA
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def setDropboxFolderData(request):
    data=request.data
    print(data)
    print(type(data))
    if(data['isRoot']==True):
        rootData=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="ROOT FOLDER DATA", provider=AllAuths.objects.get(authName="DROPBOX"))
        rootData.rootPageData['children'].append(data['dict'])
        rootData.save()

    hieData=DataAnalysis.objects.get(user=request.user, classificationOfDataStorageType="HIERARCHICAL DATA", provider=AllAuths.objects.get(authName="DROPBOX"))


    path=data['dict']['path'].split('/')
    print(path)
    # for i in range(0,len(path)):
    #     accessPath+=path[i]+"/"

    accessPath1=""  #Add To Children of this path
    for i in range(0,len(path)-1):
        accessPath1+=path[i]+"/"

    print(accessPath1)
    accessPath=data['dict']['path']+"/"
    print(accessPath)



    hieDataCopy=hieData.hierarchicalData

    #For Existing path children
    if(accessPath1 in hieDataCopy):
        hieDataCopy[accessPath1]['children'].append(dict)
    else:
        hieDataCopy[accessPath1]={}
        hieDataCopy[accessPath1]['children']=[]
        hieDataCopy[accessPath1]['children'].append(dict)


    #For new path
    hieDataCopy[accessPath]={}
    hieDataCopy[accessPath]['children']=[]
    hieDataCopy[accessPath]['children'].append(dict)

    print(type(hieDataCopy))
    #print(hieDataCopy)
    print(type(hieData.hierarchicalData))
    d=serializers.serialize('json', hieDataCopy)
    print(type(d.data))
    d1=json.loads(d)
    print(type(d1))
    hieData.hierarchicalData=json.loads(json.dumps(hieDataCopy))
    hieData.save()

    return JsonResponse({'message':'Successfully Updated Data', "status":"201"})

























#DIGITAL OCEAN
# def digitalOceanLogin(request):
#     url="https://cloud.digitalocean.com/v1/oauth/authorize"

#     return HttpResponseRedirect('/hi/complete/aws-oauth2')

# def digitalOceanComplete(request):
#     return HttpResponse("Aws Done")



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def validateUserCloud(request):
    print(request.GET.get('authName'))
    if(CloudOauth2Details.objects.filter(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName'))).count()>0):
        return JsonResponse({"message": "Success", "status":"200", "authName":request.GET.get('authName'), "access_token":CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName'))).accessToken, "auth_login_name":CloudOauth2Details.objects.get(userId=request.user, authName=AllAuths.objects.get(authName=request.GET.get('authName'))).auth_login_name})
    else:
        return JsonResponse({"message": "Error", "status":"404"})
