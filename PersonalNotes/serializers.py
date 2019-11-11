from rest_framework import serializers
from .models import savedNoteData

class savedNoteDataSerializer(serializers.ModelSerializer):

	class Meta:
		model=savedNoteData  # what module you are going to serialize
		fields= '__all__'


class savedNoteDataSerializer1(serializers.ModelSerializer):

	class Meta:
		model=savedNoteData  # what module you are going to serialize
		fields= ('noteId', 'userId', 'typeOfData', 'title', 'caption', 'createdFrom', 'createdAt', 'lastUpdated')
