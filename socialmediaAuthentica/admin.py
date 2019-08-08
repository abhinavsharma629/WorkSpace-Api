from django.contrib import admin
from .models import AllAuths,CloudOauth2Details, UserDetailsFromAuth, DataAnalysis, Notification, Trial

admin.site.register(AllAuths)
admin.site.register(CloudOauth2Details)
admin.site.register(UserDetailsFromAuth)
admin.site.register(DataAnalysis)
admin.site.register(Notification)
admin.site.register(Trial)