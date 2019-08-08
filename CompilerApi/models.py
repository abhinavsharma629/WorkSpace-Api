from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from .choices import *

class LanguageData(models.Model):
    languageChoice=models.PositiveIntegerField(choices = LANGUAGE_CHOICES, blank=True, null=True)
    problemMandatoryData=models.TextField(max_length=1000, null=True, blank=True)

class SubmissionData(models.Model):
    userId= models.ForeignKey(User, on_delete=models.CASCADE)
    problemData=models.FileField(upload_to='CompilerApi/runCode',blank=True)
    inputFile=models.FileField(upload_to='CompilerApi/runCode',blank=True, null=True)
    submissionId=models.CharField(max_length=1000, primary_key=True)
    outputFile=models.FileField(upload_to='CompilerApi/runCode',blank=True, null=True)
    status= models.CharField(max_length=100, blank=True, null=True)

class savedCodeData(models.Model):
    codeId=models.AutoField(primary_key=True)
    userId= models.ForeignKey(User, on_delete=models.CASCADE)
    problemData=models.FileField(upload_to='CompilerApi/savedCodes', blank=True)
    createdAt=models.DateTimeField(auto_now=True)
    lastUpdated=models.DateTimeField()