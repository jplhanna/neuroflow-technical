from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

#Serializer for Django/Python's REST framework
class MoodSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many = False, queryset = User.objects.all(), slug_field = 'username')
    
    #Set to handle models, specifcally the mood model created in /mood/models.py
    class Meta:
        model = Moods
        fields = ('moodScore', 'user')#Since date initializes without user input it is not included as a field
        
class StreakSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many = False, queryset = User.objects.all(), slug_field = 'username')
    
    #Set to handle models, specifcally the Streak model created in /mood/models.py
    class Meta:
        model = Streaks
        fields = ('currStreak', 'maxStreak', 'percentile', 'user')