from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

#Serializer for Django/Python's REST framework
class MoodSerializer(serializers.ModelSerializer):
    #Set to handle models, specifcally the mood model created in /mood/models.py
    class Meta:
        model = Moods
        fields = ('moodScore',)#Since date initializes without user input it is not included as a field