from rest_framework import serializers
from .models import SubmissionData, LanguageData, savedCodeData

class SubmissionDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=SubmissionData  # what module you are going to serialize
		fields= '__all__'

class LanguageDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=LanguageData  # what module you are going to serialize
		fields= '__all__'

class savedCodeDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=savedCodeData  # what module you are going to serialize
		fields= '__all__'