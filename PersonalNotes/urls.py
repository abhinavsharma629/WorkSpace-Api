from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

	# Compiler
    path('saveDeleteNote', views.saveDeleteNote.as_view()),
    path('getAllNotes', views.getAllNotes, name="getAllNotes"),
    path('getAllNotesWithLessData', views.getAllNotesWithLessData, name="getAllNotesWithLessData"),
    path('editNote', views.editNote, name="editNote"),
    path('getNoteImage', views.getNoteImage, name="getNoteImage"),
    path('submitGitHubNote', views.submitGitHubNote, name="submitGitHubNote"),

   ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)
