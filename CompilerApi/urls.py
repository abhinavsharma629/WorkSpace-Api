from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('submit',  views.submit.as_view()),
    path('getAllCode', views.getAllCode, name="getAllCode"),
    path('editCode', views.editCode, name="editCode"),
    path('saveCode', views.saveCode, name="saveCode"),
    path('getSyntax', views.getSyntax, name="getSyntax"),
    
   ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)