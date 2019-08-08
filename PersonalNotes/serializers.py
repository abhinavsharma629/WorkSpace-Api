from rest_framework import serializers
from .models import savedNoteData

class savedNoteDataSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=savedNoteData  # what module you are going to serialize
		fields= '__all__'