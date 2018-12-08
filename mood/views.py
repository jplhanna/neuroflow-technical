from django.shortcuts import render, redirect
from .models import *
from .serializer import *

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

#Currently only functionality is POST
@api_view(['POST', "GET"])
@permission_classes((permissions.AllowAny,))
def mood_list(request, format=None):
    if(request.user.username != ''):
        if request.method == 'POST': #When user attempts to POST will create a MoodSerializer object using the data input by the user
            data = request.data
            data['user'] = request.user.username
            serializer = MoodSerializer(data = data)
            if serializer.is_valid(): #If the data is valid and creates a valid object, will save the data to the SQLite database using the moods Model
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED) #Then returns a response signifying that the data was added
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Otherwise returns a bad request
        elif request.method == 'GET': 
            moods = Moods.objects.filter(user = request.user).order_by('date')
            serializer = MoodSerializer(moods, many = True)
            return Response(serializer.data)
    else:
        return redirect('/signin/')
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

@api_view(['POST','GET'])
@permission_classes((permissions.AllowAny,))
def signUp(request):
    if request.user.username == "":
        if request.method == "POST": #After a user inputs their desired user info
            user_tmp = request.data['inputUsername']
            email_tmp = request.data['inputEmail']
            password_tmp = request.data['inputPassword']
            confirm_tmp = request.data['inputPass']
            
            if(User.objects.filter(email = email_tmp).exists()): #First checks that there are no other emails with the same name
                return Response(status = status.HTTP_400_BAD_REQUEST)
            if(password_tmp == confirm_tmp): #checks that the password and it's confirmation match up
                new_user = User.objects.create_user(user_tmp, email_tmp, password_tmp)
                new_user.save()
                #If succesful will create and save user account, then log them in and redirect them to the mood endpoint
                auth_login = authenticate(username = user_tmp, password = password_tmp)
                login(request, auth_login)
                return redirect('/mood/')
            else:#Otherwise return a bad request
                return Response(status = status.HTTP_400_BAD_REQUEST)
        if request.method == "GET": #the signup endpoint gets basic information for signing up
            return Response({'inputUsername':'input username here', 'inputEmail':'input email here' , 'inputPassword':'input password here', 'inputPass':'confirm password'})
    else: #if you are signed in, get redirected to the mood endpoint
        return redirect('/mood/')
        
@api_view(['POST','GET'])
@permission_classes((permissions.AllowAny,))
def signIn(request):
    if request.user.username == "":
        if request.method == "POST": #After user posts their user info authenticates info
            user_tmp = request.data['inputUsername']
            password_tmp = request.data['inputPassword']
            check_user = authenticate(username=user_tmp, password=password_tmp)
            if check_user is not None: #if succesful, logs them in and redirects them too the mood endpoint
                login(request, check_user)
                return redirect('/mood/')
            else: #otherwise returns a bad request
                return Response(status = status.HTTP_400_BAD_REQUEST) #A future or better iteration would return something more descriptive that a front end developer can use.
        elif request.method == "GET": #the signin endpoint gets basic information for signing in
            return Response({'inputUsername':'input username here', 'inputPassword': 'input password here'})
    else: #if you are signed in, get redirected to the mood endpoint
        return redirect('/mood/')
        
def signOut(request):
    logout(request)
    return redirect('/signin/')