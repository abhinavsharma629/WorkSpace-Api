from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import friendRecommendation

urlpatterns = [

    #IP:- 127.0.0.1:8000/friends
    
    path('friendRecommendation', friendRecommendation.as_view()),
    path('createFriend/',views.createFriend, name="createFriend"),
    path('acceptFriend/',views.acceptFriend, name="acceptFriend"),
    path('cancelRequest/',views.cancelRequest, name="cancelRequest"),
    path('removeFriend/', views.removeFriend, name="removeFriend"),
    path('friendList', views.friendList, name="friendList"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)