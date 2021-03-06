from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    #Google Auth -D
    path('complete/google-oauth2/', views.complete, name="complete"),
    path('login', views.login, name="login"),
    path('gd_segregates', views.gd_segregates, name="gd_segregates"),
    path('gd_data_overview', views.gd_data_overview, name="gd_data_overview"),
    path('gd_selected_segregates', views.gd_selected_segregates, name="gd_selected_segregates"),
    path("buildDriveForDrive", views.buildDriveForDrive, name="buildDriveForDrive"),
    path('rootFolderDataForDrive', views.rootFolderDataForDrive, name="rootFolderDataForDrive"),
    path('hierarchicalFolderDataForDrive', views.hierarchicalFolderDataForDrive, name="hierarchicalFolderDataForDrive"),

    #GitHub Auth -D
    path('complete/gitHub-oauth2', views.gitHubComplete, name="gitHubComplete"),
    path('gitHubLogin', views.gitHubLogin, name="gitHubLogin"),

    #Reddit Auth -D
    path('complete/reddit-oauth2', views.redditComplete, name="redditComplete"),
    path('redditLogin', views.redditLogin, name="redditLogin"),

    #Twitter Auth -D
    path('complete/twitter-oauth2', views.twitterComplete, name="twitterComplete"),
    path('twitterLogin', views.twitterLogin, name="twitterLogin"),

    #Facebook Auth(Not Working)
    path('complete/facebook-oauth2', views.fbComplete, name="fbComplete"),
    path('fbLogin', views.fbLogin, name="fbLogin"),

    #Dropbox Auth -D
    path('complete/dropbox-oauth2', views.dropboxComplete, name="dropboxComplete"),
    path('dropboxLogin', views.dropboxLogin, name="dropboxLogin"),
    path('db_data_overview', views.db_data_overview, name="db_data_overview"),
    path('buildDropboxForDropbox', views.buildDropboxForDropbox, name="buildDropboxForDropbox"),
    path('db_segregates', views.db_segregates, name="db_segregates"),
    path('db_selected_segregates', views.db_selected_segregates, name="db_selected_segregates"),
    path('rootFolderDataForDropbox', views.rootFolderDataForDropbox, name="rootFolderDataForDropbox"),
    path('hierarchicalFolderDataForDropbox', views.hierarchicalFolderDataForDropbox, name="hierarchicalFolderDataForDropbox"),
    path('setDropboxFolderData', views.setDropboxFolderData, name="setDropboxFolderData"),
    path('deleteDropboxFolderData', views.deleteDropboxFolderData, name="deleteDropboxFolderData"),
    path('setDropboxFileData', views.setDropboxFileData, name="setDropboxFileData"),
    path('deleteDropboxFileData', views.deleteDropboxFileData, name="deleteDropboxFileData"),
    
    #OneDrive Auth / #Microsoft Azure -D
    path('complete/oneDrive-oauth2', views.oneDriveComplete, name="oneDriveComplete"),
    path('oneDriveLogin', views.oneDriveLogin, name="oneDriveLogin"),
    path('complete/oneDrive-oauth21', views.oneDriveComplete1, name="oneDriveComplete1"),
    path('ma_data_overview', views.ma_data_overview, name="ma_data_overview"),
    #Digital Ocean Auth
    # path('complete/digitalOcean-oauth2', views.digitalOceanComplete, name="digitalOceanComplete"),
    # path('digitalOceanLogin', views.digitalOceanLogin, name="digitalOceanLogin"),

    #Alibaba Auth
    #Aws Auth
    path('index', views.index, name="index"),
    path('folderView', views.folderView, name="folderView"),

    path('compareUserProfiles', views.compareUserProfiles, name="compareUserProfiles"),

    path('index1', views.index1, name="index1"),
    path('folderView1', views.folderView1, name="folderView1"),

    path('fileDownload', views.fileDownload, name="fileDownload"),
    path('gitHubfolderView', views.gitHubfolderView, name="gitHubfolderView"),
    path('repo', views.repo, name="repo"),
    path('friendRepos/<username>', views.friendRepos, name="friendRepos"),
    path('friendRepoDetails/<username>', views.friendRepoDetails, name="friendRepoDetails"),
    path('friendList', views.friendList, name="friendList"),
    path('compareProfiles', views.compareProfiles, name="compareProfiles"),
    path('validateUserCloud', views.validateUserCloud, name="validateUserCloud"),
    path('buildDrive', views.buildDrive, name="buildDrive"),
    path('storeCloud', views.storeCloud, name="storeCloud"),
    path('socialLogout', views.socialLogout, name="socialLogout"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
