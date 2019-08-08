from django.contrib import admin
from .models import sharedNoteData, CommentsOnNotes, NotesDetails

admin.site.register(sharedNoteData)
admin.site.register(CommentsOnNotes)
admin.site.register(NotesDetails)