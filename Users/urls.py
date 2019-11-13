# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.contrib.auth.views import LogoutView
# from django.views.generic import TemplateView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('', include('social_django.urls', namespace='social')),
#     path('all/', include('allauth.urls')),
#     path('index', TemplateView.as_view(template_name="socialmediaAuthentication/index.html")),
#     path('logout', LogoutView.as_view(template_name=''), name="logout"),
#     path('hi/', include('socialmediaAuthentication.urls')),
# ]

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    #IP:- 127.0.0.1:8000/user

    path('getUserDetails/', views.getUserDetails, name="getUserDetails"),
    path('userValidity', views.userValidity, name="userValidity"),
    path('editUserDetails/', views.editUserDetails, name="editUserDetails"),
    path('deleteUserDetails/', views.deleteUserDetails, name="deleteUserDetails"),
    path('createUser/', views.createUser, name="createUser"),
    path('saveImage/', views.saveImage, name="saveImage"),
    path('createFullUser/', views.createFullUser, name="createFullUser"),
    path('validateUser/', views.validateUser, name="validateUser"),

    # Your URLs...
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
