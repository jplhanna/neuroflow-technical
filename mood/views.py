from django.shortcuts import render
from .models import *
from .serializer import *

from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

#Currently only functionality is POST
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def mood_list(request, format=None):
    if request.method == 'POST': #When user attempts to POST will create a MoodSerializer object using the data input by the user
        serializer = MoodSerializer(data = request.data)
        if serializer.is_valid(): #If the data is valid and creates a valid object, will save the data to the SQLite database using the moods Model
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #Then returns a response signifying that the data was added
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Otherwise returns a bad request
    #elif request.method == 'GET':
    #    moods = Moods.objects.all()
    #    serializer = MoodSerializer(moods, many = True)
    #    return Response(serializer.data)
'''
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def mood_detail(request, pk):
    mood = Moods.objects.get(pk = pk)
    
    if request.method == 'GET':
        serializer = MoodSerializer(mood)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MoodSerializer(mood, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        mood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''