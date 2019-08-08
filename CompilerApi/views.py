#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubmissionData, LanguageData, savedCodeData
from .serializers import SubmissionDataSerializer, LanguageDataSerializer, savedCodeDataSerializer
from django.db.models import Q
from django.http import JsonResponse
# from .tasks import submission
from rest_framework.parsers import MultiPartParser
from django.core import serializers
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


#Problem Submit And Get Status
class submit(APIView):
    permission_classes=(IsAuthenticated,)
    #GET
    def get(self, request):
        subId=request.GET.get('subId')
        print(subId)

        #Try if submission Id exists
        try:
            userDetails=SubmissionData.objects.get(submissionId=subId)
        except Exception as e:
            #print(e)
            return Response({"message" :"No Such Id"}, status=status.HTTP_404_NOT_FOUND)
        
        if(userDetails.status=="Not Judged"):
            return Response({"message" :"Result Not Generated Yet"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer= SubmissionDataSerializer(userDetails)
            userDetails.delete()
            return Response({"message":"Ok Done", "data":serializer.data}, status=status.HTTP_200_OK)
    
    
    #POST
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        params=request.data
        user=params['user']
        file=params['file']
        print(file)
        c=False
        
        try:
            inputFile=params['inputFile']
            c=True
        except:
            c=False
        
        #print(user, type(user))
        file_ext_check=file.name.split(".")[1]
        print(file_ext_check)
        #print(file_ext_check)
        if(file_ext_check=='java' or file_ext_check=='c' or file_ext_check=='cpp' or file_ext_check=='py'):
            if(file_ext_check == 'java'):
                language=1
            elif(file_ext_check == 'cpp'):
                language=2
            elif(file_ext_check == 'c'):
                language=3
            elif(file_ext_check == 'py'):
                language=4
            print(language)
            
            #stat = submission.delay(language)
            stat="dfff"
            print(stat)
            if(c):
                obj,notif=SubmissionData.objects.get_or_create(userId=request.user, problemData=file, inputFile=inputFile, submissionId=stat, status="Not Judged")
            else:
                obj,notif=SubmissionData.objects.get_or_create(userId=request.user, problemData=file, submissionId=stat, status="Not Judged")
            print(notif)
            if notif is True:
                obj.save()

        else:
            return Response({"message": "Language Not Supported"}, status=status.HTTP_404_NOT_FOUND)

        #Till Submission Result is not generated or more than 5 seconds is taken:- 
        import time
        startTime=time.time()
        time1=0
        while(SubmissionData.objects.get(submissionId=stat).status=="Not Judged" and time1-startTime<=5):
            print(time1-startTime)
            time1=time.time()
        if(SubmissionData.objects.filter(submissionId=stat).count()>0):
            data=SubmissionDataSerializer(SubmissionData.objects.get(submissionId=str(stat)))
            #data=serializers.serialize('json', SubmissionData.objects.get(submissionId=stat))
            SubmissionData.objects.get(submissionId=stat).delete()
            return Response({"message":"Ok Done" , "data": data.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Error"}, status=status.HTTP_404_NOT_FOUND)
    



#GET Language Syntax params:- probId:- [1-Java, 2- C++, 3- C, 4- Py 3+]
@api_view(['GET'])
def getSyntax(request):

    data=request.GET.get('probId')
    print(data)
    syntaxData=LanguageData.objects.get(languageChoice=data)
    #print(syntaxData)
    #print(syntaxData.languageChoice, syntaxData.problemMandatoryData)
    serializer= LanguageDataSerializer(syntaxData)
    print(serializer.data)
    return Response({"message":"Ok Done", "data":serializer.data}, status=status.HTTP_200_OK)
    #return JsonResponse({'data':'1'})


#POST
@api_view(['POST'])
def editCode(request):
    parser_classes = (MultiPartParser,)
    permission_classes=(IsAuthenticated,)
    params=request.data
    #user=params['user']
    codeId=params['codeId']
    file=params['file']
    
    try:
        obj=savedCodeData.objects.get(codeId=codeId)
        obj.problemData=file
        obj.lastUpdated=timezone.now()
        obj.save()
        data=savedCodeDataSerializer(obj)
        stat=status.HTTP_201_CREATED
        return Response({"message": "Ok Edited", 'data': data.data}, stat)
    except:
        stat=status.HTTP_404_NOT_FOUND
        return Response({"message": "Error"}, stat)
    
    #To serialize all data of the particular user at once
    # serializer = serializers.serialize('json', savedCodeData.objects.all(), fields=('codeId', 'username','problemData', 'createdAt', 'lastUpdated'))
        
    # print(serializer)
    # return Response(serializer, status=stat)


@api_view(['GET'])
def getAllCode(request):
    permission_classes=(IsAuthenticated,)
    try:
        data=savedCodeData.objects.filter(userId=User.objects.get(username=request.GET.get('userId')))
        serializedData=savedCodeDataSerializer(data, many=True)
        return Response({"message":"Ok", "data":serializedData.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Error- "+str(e)}, status=status.HTTP_404_NOT_FOUND)



#POST
@api_view(['POST'])
def saveCode(request):
    parser_classes = (MultiPartParser,)
    permission_classes=(IsAuthenticated,)
    params=request.data
    #user=params['user']
    file=params['file']
    
    try:
        obj,notif=savedCodeData.objects.get_or_create(userId=request.user, problemData=file, lastUpdated=timezone.now())
        if(notif is True):
            obj.save()
        print(obj.codeId)
        stat=status.HTTP_201_CREATED
        serializer=savedCodeDataSerializer(obj)
        return Response({"message": "Ok Saved", 'data': serializer.data}, stat)
    except:
        stat=status.HTTP_400_BAD_REQUEST
        return Response({"message": "Error"}, stat)