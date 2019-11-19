import json
import requests
from django.contrib.auth.models import User
from .models import AllAuths, DataAnalysis


provider=AllAuths.objects.get(authName='DROPBOX')

def dropBoxTree1(accessToken, username):
	obj=User.objects.get(username=username)

	url = "https://api.dropboxapi.com/2/files/list_folder"

	payload = "{\r\n    \"path\": \"\",\r\n    \"recursive\": true,\r\n    \"include_media_info\": true,\r\n    \"include_deleted\": false,\r\n    \"include_has_explicit_shared_members\": true,\r\n    \"include_mounted_folders\": true,\r\n    \"include_non_downloadable_files\": true\r\n}"

	headers = {
	    'Content-Type': "application/json",
	    'Authorization': "Bearer "+accessToken,
	    'User-Agent': "PostmanRuntime/7.15.0",
	    'Accept': "*/*",
	    'Cache-Control': "no-cache",
	    'Postman-Token': "70872dce-675e-47ef-98c2-bb39391fa3ae,854d6fcb-1d05-467a-99f1-5e7366e53935",
	    'Host': "api.dropboxapi.com",
	    'accept-encoding': "gzip, deflate",
	    'content-length': "241",
	    'Connection': "keep-alive",
	    'cache-control': "no-cache"
	    }
	hasMore=True
	currentCursor=""
	dataAnalysis={}
	folderDict={}
	entries=[]
	rootDict={}
	rootDict['children']=[]
	dropBoxMyDict={}
	segregatedDataDict={}
	folderDataDict={}
	picTypes=['jpg', 'jpeg', 'png', 'gif', 'tif']

	while(hasMore==True):
		response = requests.request("POST", url, data=payload, headers=headers).json()
		currentCursor=response['cursor']
		hasMore=True if(response['has_more']=="true") else False
		url = "https://api.dropboxapi.com/2/files/list_folder/continue"

		print(json.dumps(response, indent=4))

		for i in response['entries']:
			myDict={}
			myDict['typeOfFile']=i['.tag']
			myDict['name']=i['name']
			myDict['path']=i['path_display']
			myDict['id']=i['id'].split(':')[1]

			if('client_modified' in i):
				myDict['clientModifiedDate']=i['client_modified']

			if('server_modified' in i):
				myDict['serverModifiedDate']=i['server_modified']

			if('size' in i):
				myDict['size']=i['size']

			if('is_downloadable' in i):
				myDict['canBeDownload']=i['is_downloadable']

			if('has_explicit_shared_members' in i):
				myDict['hasSharedMembers']=i['has_explicit_shared_members']

			if('content_hash' in i):
				myDict['uniqueHash']=i['content_hash']

			if('media_info' in i):
				mediaInfo={}
				mediaInfo['metaTag']=i['media_info']['metadata']['.tag']
				mediaInfo['dimensions']={}
				mediaInfo['dimensions']['height']=i['media_info']['metadata']['dimensions']['height']
				mediaInfo['dimensions']['width']=i['media_info']['metadata']['dimensions']['width']
				mediaInfo['timeOfPhoto']=i['media_info']['metadata']['time_taken']
				myDict['mediaInfo']=mediaInfo

			#Making Parent Child Relation:-
			treePath=myDict['path'].split('/')
			lastElement=len(treePath[len(treePath)-1])
			currentPath=myDict['path'][0:len(myDict['path'])-lastElement]

			if(currentPath=="/"):
				rootDict['children'].append(myDict)

			if(currentPath in dropBoxMyDict):
				dropBoxMyDict[currentPath]['children'].append(myDict)

			else:
				dropBoxMyDict[currentPath]={}
				dropBoxMyDict[currentPath]['children']=[]
				dropBoxMyDict[currentPath]['children'].append(myDict)

			if(myDict['typeOfFile']!="folder"):
				file_ext=i['name'].split(".")[len(i['name'].split("."))-1]
				print(file_ext)
				if(file_ext in segregatedDataDict):
					segregatedDataDict[file_ext].append(myDict)

				else:
					segregatedDataDict[file_ext]=[]
					segregatedDataDict[file_ext].append(myDict)

			if(myDict['typeOfFile']=="folder"):
				folderDataDict[myDict['path']]=myDict


	#f=open('dropBoxAnalysis.json','w')
	#json.dump(dropBoxMyDict, f)
	#f.close()
	print(json.dumps(segregatedDataDict, indent=4))







	#Create / Update Only Folder Data
	try:
		folderData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA")
		folderData.folderData=folderDataDict
		folderData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA" , folderData=folderDataDict)
		if(notif):
			objec.save()


	#Create / Update Only Root Page Data
	try:
		rootPageData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA")
		rootPageData.rootPageData=rootDict
		rootPageData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA" , rootPageData=rootDict)
		if(notif):
			objec.save()

	#Create / Update Only Hierarchical Data
	try:
		hierarchicalData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA")
		hierarchicalData.hierarchicalData=dropBoxMyDict
		hierarchicalData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA" , hierarchicalData=dropBoxMyDict)
		if(notif):
			objec.save()
    

	#Create / Update Only Segregated Data
	for i,j in segregatedDataDict.items():
		try:
			segregatedData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA", typeOfData=i)
			segregatedData.segregatedData=segregatedDataDict[i]
			segregatedData.save()
		except:
			objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA" , typeOfData=i, segregatedData=segregatedDataDict[i])
			if(notif):
				objec.save()
