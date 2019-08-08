import json
import requests
from django.contrib.auth.models import User
provider="sdf"

def googleTree(access_token, username):
	obj=User.objects.get(username=username)
	dataAnalysis={}
	folderDict={}

	headers = {
			    'Authorization': "Bearer "+access_token,
			    'cache-control': "no-cache",
			    'Postman-Token': "058d5b8f-4536-4c0a-a91f-03bafac54b77"
			    }


	hasNextPage=1
	nextPageToken=0
	finalDict={}
	searchItemsDict={}
	c=False
	rootFolder={}
	ad=[]
	while(hasNextPage>0):
		#If next page Exists
		if(nextPageToken==0):
			url="https://www.googleapis.com/drive/v2/files?maxResults=1000&orderBy=createdDate"
		else:
			url="https://www.googleapis.com/drive/v2/files?maxResults=1000&orderBy=createdDate&pageToken="+str(nextPageToken)
		
		response=requests.get(url,headers=headers)
		response=response.json()

		# print(json.dumps(response, indent=4))
		# f1=open('googleCompareFinalDict.json','w')
		# json.dump(response, f1)
		# f1.close()
		
		#response['incompleteSearch']=False
		#print(type(response['incompleteSearch']))
		#If next page Exists
		if('nextPageToken' in response):
			nextPageToken=response['nextPageToken']
		else:
			hasNextPage=0
		

		for i in response['items']:
			finalDict[i['id']]={}
			finalDict[i['id']]['childId']=i['id']
			finalDict[i['id']]['embedLink']=i['embedLink']
			finalDict[i['id']]['selfLink']=i['selfLink']
			finalDict[i['id']]['alternateLink']=i['alternateLink']
			finalDict[i['id']]['title']=i['title']

			mimeType=i['mimeType']

			typeof=mimeType.split('.')
			typeOfFile=typeof[len(typeof)-1]
			
			
			finalDict[i['id']]['type']=typeOfFile

			if('parents' in i and len(i['parents'])>0):
				#print(type(i['parents'][0]['isRoot']))
				if(i['parents'][0]['isRoot']==False):
					#print("yes")
					if(i['parents'][0]['id'] in searchItemsDict):
						#print("yes1")
						searchItemsDict[i['parents'][0]['id']].append(i['id'])
					else:
						#print("yes2")
						searchItemsDict[i['parents'][0]['id']]=[]
						searchItemsDict[i['parents'][0]['id']].append(i['id'])
				else:
					finalDict[i['id']]['children']=[]
					c=True
			else:
				finalDict[i['id']]['children']=[]
			
			finalDict[i['id']]['created']=i['createdDate']
			finalDict[i['id']]['modifiedDate']=i['modifiedDate']
			finalDict[i['id']]['version']=i['version']
			finalDict[i['id']]['owners']=i['ownerNames']
			#finalDict[i['id']]['lastModifyingUserName']=i['lastModifyingUserName']
			finalDict[i['id']]['editable']=i['editable']
			finalDict[i['id']]['children']=[]

			if(typeOfFile in dataAnalysis and typeOfFile!="folder"):
				dataAnalysis[typeOfFile].append(finalDict[i['id']])
			elif(typeOfFile!="folder"):
				dataAnalysis[typeOfFile]=[]
				dataAnalysis[typeOfFile].append(finalDict[i['id']])

			#Root Folder Files
			if(c==True):
				rootFolder[i['id']]=[]
				rootFolder[i['id']].append(finalDict[i['id']])
				c=False

			if(finalDict[i['id']]['type']=="folder"):
				folderDict[i['id']]={}
				folderDict[i['id']]=finalDict[i['id']]

			

	# print(finalDict)
			
	for i,j in searchItemsDict.items():
		try:
			finalDict[i]['children']=j
		except Exception as e:
			print(e)
	
	# f4=open('searchDict.json', 'w')
	# json.dump(searchItemsDict, f4)
	# f4.close()	

	print(finalDict)
	f=open('googleFinalDict.json','w')
	json.dump(finalDict, f)
	f.close()

	
	#Giving Unknown and error that i couldn't understand
	
	# for i,j in searchItemsDict.items():
	# 	if(i in folderDict):
	# 		folderDict[i]['children']=[]
	# 	for k in j:
	# 		if(finalDict[k]['type']=="folder"):
	# 			folderDict[i]['children'].append(k)
		
	
	# print("Root Folder Files:- ")
	# print(json.dumps(rootFolder, indent=4))
	# print("----------------------------------------------------")
	# print("----------------------------------------------------")
	# print("Root Folder Length:- ")
	# print(len(rootFolder))
	# print("----------------------------------------------------")
	# print("----------------------------------------------------")
	# print("\n\n\n\n\n\n\n")





	# print(json.dumps(finalDict, indent=4))
	# print("\n\n\n\n\n\n\n")
	# print("----------------------------------------------------")
	# print("----------------------------------------------------")
	# print("\n\n\n\n\n\n\n")
	# print("Id's of Folders with children Are:- ")
	# print("----------------------------------------------------")
	

	#Create / Update Only Folder Data
	try:
		folderData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA")
		folderData.folderData=folderDict
		folderData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="FOLDER DATA" , folderData=folderDict)
		if(notif):
			objec.save()


	#Create / Update Only Root Page Data
	try:
		rootPageData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA")
		rootPageData.rootPageData=rootFolder
		rootPageData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="ROOT FOLDER DATA" , rootPageData=rootFolder)
		if(notif):
			objec.save()

	#Create / Update Only Hierarchical Data
	try:
		hierarchicalData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA")
		hierarchicalData.hierarchicalData=finalDict
		hierarchicalData.save()
	except:
		objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="HIERARCHICAL DATA" , hierarchicalData=finalDict)
		if(notif):
			objec.save()


	for i in finalDict:
		try:
			if(len(finalDict[i]['children'])>0):
				print("Id:- ", i,";  ", "Number of Children:- ", len(finalDict[i]['children']))
				print("\n")
		except Exception as e:
			print(e)


	
	
	#Create / Update Only Segregated Data
	for i,j in dataAnalysis.items():
		data={}
		data[i]=dataAnalysis[i]
		try:
			segregatedData=DataAnalysis.objects.get(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA", typeOfData=i)
			segregatedData.segregatedData=data
			segregatedData.save()
		except:
			objec,notif=DataAnalysis.objects.get_or_create(user=obj, provider=provider, classificationOfDataStorageType="SEGREGATED DATA" , typeOfData=i, segregatedData=data)
			if(notif):
				objec.save()