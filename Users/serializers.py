from rest_framework import serializers
from .models import UserDetails

class UserDetailsSerializer(serializers.ModelSerializer):
	username=serializers.CharField(source='userId.username')
	class Meta:
		model=UserDetails  # what module you are going to serialize
		fields= ('username','userId', 'address', 'address1', 'phoneNumber', 'occupation', 'state', 'city', 'country', 'alternatePhoneNumber', 'profilePhoto', 'coverPhoto', 'dateOfBirth', 'gender', 'current_lat', 'current_long')