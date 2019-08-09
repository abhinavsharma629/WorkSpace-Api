import json
import requests
from django.contrib.auth.models import User
from .models import AllAuths, DataAnalysis

provider=AllAuths.objects.get(authName='GITHUB')

def getGitHubNotifications(username, access_token):
    obj=User.objects.get(username=username)
    
    #GET All Notifications Url
    url = "https://api.github.com/notifications"

    headers = {
        'Authorization': "Bearer "+access_token,
        'Host': "api.github.com"
        }

    response = requests.request("GET", url, headers=headers).json()

    print(response.json())

    #URL For Specific Notifications
    #https://api.github.com/notifications?since=2019-07-12T24:00:00Z