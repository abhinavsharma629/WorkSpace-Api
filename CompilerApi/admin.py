from django.contrib import admin
from .models import SubmissionData, LanguageData, savedCodeData

admin.site.register(LanguageData)
admin.site.register(SubmissionData)
admin.site.register(savedCodeData)