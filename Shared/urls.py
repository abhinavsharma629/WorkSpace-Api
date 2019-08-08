from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    
	# 127.0.0.1:8000/shared
    path('shareNote/', views.shareNote, name="shareNote"),
    path('deleteSharedNote/', views.deleteSharedNote, name="deleteSharedNote"),
    path('noteSharedTo', views.noteSharedTo, name="noteSharedTo"),
    path('getFriends', views.getFriends, name="getFriends"),
    path('sharedNotes', views.sharedNotes, name="sharedNotes"),
    path('commentOnNote', views.commentOnNote.as_view()),
    path('likeOnNote', views.likeOnNote.as_view()),
    path('noteDetails',views.noteDetails, name="noteDetails"),
    path('selfSharedNoteDetails', views.selfSharedNoteDetails, name="selfSharedNoteDetails"),
    path('specificNoteDetail', views.specificNoteDetail, name="specificNoteDetail"),
    path('allUserFriends', views.allUserFriends, name="allUserFriends"),
    path('specificNoteDetailForGit', views.specificNoteDetailForGit, name="specificNoteDetailForGit"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns=format_suffix_patterns(urlpatterns)