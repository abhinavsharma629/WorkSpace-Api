from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField, JSONField, HStoreField #HStoreField has many custom lookups available
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .authChoices import AUTH_CHOICES
from .FIELD_CHOICES import FIELD_CHOICES


class AllAuths(models.Model):
    authName=models.CharField(choices=AUTH_CHOICES, primary_key=True, max_length=1000, null=False, blank=False)
    clientId=models.CharField(max_length=1000)
    clientSecret=models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.authName

class CloudOauth2Details(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE)
    authName=models.ForeignKey(AllAuths, on_delete=models.CASCADE, db_column="authName") #By default, Django populates column's name by appending _id to the field name you define in your model. You must explicitly specify column's name using  db_column property as follows:
    auth_login_name=models.CharField(max_length=100, null=True, blank=True)
    revokeTokenUri=models.URLField(null=True)
    accessToken=models.CharField(max_length=10000, null=False)
    refreshToken=models.CharField(max_length=10000, null=True)
    tokenExpiry=models.DateTimeField(default=timezone.now()+timedelta(minutes=60))
    idTokenJwt=models.CharField(max_length=10000, null=True)
    tokenId=models.CharField(max_length=10000, null=True)
    tokenInfoUri=models.URLField(null=True)
    accessData=JSONField(null=True)

    def __str__(self):
        return "Cloud Oauth2 Details For:- "+self.userId.username+" - "+self.authName.authName


class UserDetailsFromAuth(models.Model):
    userId=models.OneToOneField(User,on_delete=models.CASCADE)
    authName=models.ForeignKey(AllAuths, on_delete=models.CASCADE, db_column="authName")
    userDetailsJson=HStoreField(null=True)

    def __str__(self):
        return self.userId.username+" - "+self.authName

    ''' Used One to One instead of foreign key as socialmediaAuthentication.CloudOauth2Details.userId: (fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
	HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.'''

class DataAnalysis(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    provider=models.ForeignKey(AllAuths, on_delete=models.CASCADE)
    classificationOfDataStorageType=models.CharField(choices=FIELD_CHOICES, max_length=100, null=True, blank=True)
    typeOfData=models.CharField(max_length=100, null=True, blank=True)
    segregatedData=JSONField(null=True, blank=True)
    rootPageData=JSONField(null=True, blank=True)
    hierarchicalData=JSONField(null=True, blank=True)
    folderData=JSONField(null=True, blank=True)
    analysisData=JSONField(null=True, blank=True)

    def __str__(self):
        if(self.segregatedData):
            data="Segregated Data"
        elif(self.rootPageData):
            data="RootPage Data"
        elif(self.hierarchicalData):
            data="Hierarchical Data"
        elif(self.folderData):
            data="Folder Data"
        elif(self.analysisData):
            data="Analysis Data"
        else:
            data=""

        return self.user.username+" - "+self.provider.authName+" - "+data


class Notification(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    provider=models.ForeignKey(AllAuths, on_delete=models.CASCADE)
    date=models.DateTimeField()
    isRead=models.BooleanField(default=False)
    notificationData=JSONField(null=True, blank=True)

class Trial(models.Model):
    username=models.CharField(max_length=100, null=True, blank=True)
    date=models.DateTimeField(auto_now=True)
    isRead=models.BooleanField(default=False)
    userRepos=JSONField(null=True, blank=True)
    url=models.URLField(null=True, blank=True)
    analysisDict=JSONField(null=True, blank=True)
