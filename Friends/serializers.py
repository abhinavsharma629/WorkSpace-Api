from rest_framework import serializers
from .models import FriendsFormedDetails, UserFriends
from django.contrib.auth.models import User

class FriendsFormedDetailsSerializer(serializers.ModelSerializer):
	username=serializers.CharField(source='user.userId.username')
	friends_name=serializers.CharField(source='friend_name.userId.username')
	#username = serializers.RelatedField(source='logged_in_user.username', read_only=True)
	#friends_name = serializers.RelatedField(source='current_user_friends.username', read_only=True)
	
	class Meta:
		model=FriendsFormedDetails  # what module you are going to serialize
		fields= ('username', 'friends_name', 'formedAt','friend_or_Request', 'access')

class UserFriendsSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=UserFriends  # what module you are going to serialize
		fields= '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User  # what module you are going to serialize
		fields= ('username')
		
class UserFriendsWithDetailsSerializer(serializers.ModelSerializer):
	friends=FriendsFormedDetailsSerializer(many=True)
	user=serializers.CharField(source="userId.username")
	class Meta:
		model=UserFriends  # what module you are going to serialize
		fields= ('user', 'friends')