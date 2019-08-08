from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    #IP:- 127.0.0.1:8000
    
    path('admin/', admin.site.urls),
    path('compilerApi/', include('CompilerApi.urls')),
    path('personalNotes/', include('PersonalNotes.urls')),
    path('hi/', include('socialmediaAuthentica.urls')),
    path('user/', include('Users.urls')),
    path('friends/',include('Friends.urls')),
    path('shared/',include('Shared.urls')),
    path('notif/',include('Notifications.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


