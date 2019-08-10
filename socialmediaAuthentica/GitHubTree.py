import json
import requests
from django.contrib.auth.models import User
from .models import AllAuths, DataAnalysis

provider=AllAuths.objects.get(authName='GITHUB')

def gitHubTree(access_token, username, user):
    obj=User.objects.get(username=username)
    print(user)
    print("Access token is:- ",access_token)
    print("Git User is", user)

    headers = {
		'Authorization': "Bearer "+access_token,
		'cache-control': "no-cache"
		}

    url = "https://api.github.com/user/repos"
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
        response = requests.request("GET", url1, headers=headers).json()
        print(len(response))
        print(response)
        if(len(response)>0):
            for i in response:
                currentRepoDict=i
   
                languageDetailsUrl = "https://api.github.com/repos/"+user+"/"+currentRepoDict['name']+"/languages"

                languageDetailsHeader = {
                    'Authorization': "Bearer "+access_token,
                    'Host': "api.github.com"
                    }

                languageResponse = requests.request("GET", languageDetailsUrl, headers=languageDetailsHeader).json()
                
                #print(languageResponse)
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
    
    f=open('gitHubAnalysis.json', 'w')
    json.dump(gitHubRepoDict, f)
    f.close()
    
    
    # #Create / Update Only Folder Data
    # try:
	# 	folderData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA")
	# 	folderData.folderData=folderDataDict
	# 	folderData.save()
	# except:
	# 	objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA" , folderData=folderDataDict)
	# 	if(notif):
	# 		objec.save()


	#Create / Update Only Root Page Data
    try:
        rootPageData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA")
        rootPageData.rootPageData=gitHubRepoDict
        rootPageData.save()
        
    except:
        objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA" , rootPageData=gitHubRepoDict)
        if(notif):
            objec.save()

	# #Create / Update Only Hierarchical Data
    # try:
	# 	hierarchicalData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA")
	# 	hierarchicalData.hierarchicalData=dropBoxMyDict
	# 	hierarchicalData.save()
    # except:
	# 	objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA" , hierarchicalData=dropBoxMyDict)
	# 	if(notif):
	# 		objec.save()

	
	#Create / Update Only Segregated Data
    for i,j in languageSegregationDict.items():
        #print(i)
        #print(languageSegregationDict[i])
        try:
            segregatedData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA", typeOfData=i)
            segregatedData.segregatedData=languageSegregationDict[i]
            segregatedData.save()
        
        except:
            objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA" , typeOfData=i, segregatedData=languageSegregationDict[i])
            if(notif):
                objec.save()


    #Create / Update Only Analysis Data
    try:
        rootPageData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="ANALYSIS DATA")
        rootPageData.analysisData=analysisDict
        rootPageData.save()
        
    except:
        objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="ANALYSIS DATA" , analysisData=analysisDict)
        if(notif):
            objec.save()