import json
import requests

def userRepo(username, access_token):
    print(username)
    url = "https://api.github.com/users/"+username+"/repos"
    currentPage=1
    dataLength=1
    gitHubRepoDict={}
    userPrivateDict={}
    userPublicDict={}
    totalOfLanguages={}
    forkedDict={}
    languageSegregationDict={}
    analysisDict={}

    while(dataLength>0):
        url1=url+"?page="+str(currentPage)
        headers = {
		'Authorization': "Bearer "+access_token,
		'cache-control': "no-cache"
		}
        response = requests.request("GET", url1, headers=headers).json()

        if(len(response)>0):
            for i in response:
                currentRepoDict=i
                #print(currentRepoDict)
                languageDetailsUrl = "https://api.github.com/repos/"+username+"/"+currentRepoDict['name']+"/languages"
                headers = {
                'Authorization': "Bearer "+access_token,
                'cache-control': "no-cache"
                }
                languageResponse = requests.request("GET", languageDetailsUrl, headers=headers).json()

                sum=0
                #Get lang sum
                for i,j in languageResponse.items():
                    sum+=j
                #Get Lang %
                for i,j in languageResponse.items():
                    languageResponse[i]=(j/sum)*100

                    #Get per lang Total
                    if(i in analysisDict):
                        analysisDict[i]['count']+=1
                        analysisDict[i]['total']+=(j/sum)*100
                    else:
                        analysisDict[i]={
                            'total':(j/sum)*100,
                            'count': 1
                        }

                    if(i in totalOfLanguages and currentRepoDict['fork']=="false"):
                        totalOfLanguages[i]['value']+=(j/sum)*100

                    elif((not i in totalOfLanguages) and currentRepoDict['fork']=="false"):
                        totalOfLanguages[i]={
                            'value':(j/sum)*100,
                            'count': 1
                        }

                #All Repo Dict
                gitHubRepoDict[currentRepoDict['id']]=currentRepoDict

                owner=currentRepoDict['owner']['login']
                id=currentRepoDict['owner']['id']
                gitHubRepoDict[currentRepoDict['id']]['owner']={
                    'ownerName':owner,
                    'id':id
                }
                gitHubRepoDict[currentRepoDict['id']]['language1']=languageResponse

                #Only Forked Repo Dict
                if(currentRepoDict['fork']=="true"):
                    forkedDict[currentRepoDict['id']]=currentRepoDict
                    forkedDict[currentRepoDict['id']].pop('owner')
                    forkedDict[currentRepoDict['id']]['owner']={
                        'ownerName':owner,
                        'id':id
                    }
                    forkedDict[currentRepoDict['id']]['language1']=languageResponse

                #Only Private Repo Dict
                elif(currentRepoDict['private']=="true"):
                    userPrivateDict[currentRepoDict['id']]=currentRepoDict
                    userPrivateDict[currentRepoDict['id']].pop('owner')
                    userPrivateDict[currentRepoDict['id']]['owner']={
                        'ownerName':owner,
                        'id':id
                    }
                    userPrivateDict[currentRepoDict['id']]['language1']=languageResponse

                #Only Public Repo Dict
                else:
                    userPublicDict[currentRepoDict['id']]=currentRepoDict
                    userPublicDict[currentRepoDict['id']].pop('owner')
                    userPublicDict[currentRepoDict['id']]['owner']={
                        'ownerName':owner,
                        'id':id
                    }
                    userPublicDict[currentRepoDict['id']]['language1']=languageResponse

                #print(json.dumps(gitHubRepoDict, indent=4),'\n\n-----------\n\n')
                if(gitHubRepoDict[currentRepoDict['id']]['language'] in languageSegregationDict):
                    languageSegregationDict[gitHubRepoDict[currentRepoDict['id']]['language']]['repos'].append(gitHubRepoDict[currentRepoDict['id']])
                else:
                    languageSegregationDict[gitHubRepoDict[currentRepoDict['id']]['language']]={}
                    languageSegregationDict[gitHubRepoDict[currentRepoDict['id']]['language']]['repos']=[]
                    languageSegregationDict[gitHubRepoDict[currentRepoDict['id']]['language']]['repos'].append(gitHubRepoDict[currentRepoDict['id']])

        else:
            dataLength=0
            break
        currentPage+=1

    return [gitHubRepoDict,analysisDict]

def userFollowing(username):
    followingDict={}
    url="https://api.github.com/users/"+username+"/following"
    headers = {
		'Authorization': "Bearer e232f00eb7027b8cfa4e0907270fd4613b3401c5",
		'cache-control': "no-cache"
		}
    followingDict['followingUsers']=requests.request("GET", url, headers=headers).json()
    return followingDict

def userFollowers(username):
    followerDict={}
    url="https://api.github.com/users/"+username+"/followers"
    headers = {
		'Authorization': "Bearer e232f00eb7027b8cfa4e0907270fd4613b3401c5",
		'cache-control': "no-cache"
		}
    followerDict['followers']=requests.request("GET", url, headers=headers).json()
    #print(followerDict)
    return followerDict
