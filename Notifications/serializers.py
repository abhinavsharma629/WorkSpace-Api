from rest_framework import serializers
from .models import Notifications

class NotificationsSerializer(serializers.ModelSerializer):
    fromUser=serializers.CharField(source='fromUser.userId.username')
    toUser=serializers.CharField(source='toUser.userId.username')
    
    class Meta:
        model=Notifications  # what module you are going to serialize
        fields= ('fromUser', 'toUser', 'notification', 'date', 'isRead')