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
    path('gd_login_auth_uri', views.gd_login_auth_uri, name="gd_login_auth_uri"),

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

    #OneDrive Auth / #Microsoft Azure -D
    path('complete/oneDrive-oauth2', views.oneDriveComplete, name="oneDriveComplete"),
    path('oneDriveLogin', views.oneDriveLogin, name="oneDriveLogin"),

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
