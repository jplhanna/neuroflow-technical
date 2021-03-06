from django.shortcuts import render, redirect
from .models import *
from .serializer import *
from .moodhelper import *
from .permissions import *

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from rest_framework import status, generics, viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response


#Currently functionality is POST and GET
'''
@api_view(['POST', "GET"])
@permission_classes((permissions.AllowAny,))
def mood_list(request, format=None):
    if(request.user.username != ''):
        if request.method == 'POST': #When user attempts to POST will create a MoodSerializer object using the data input by the user
            data = request.data
            data['user'] = request.user.username #Adds username to collected data

            #Checks if this new POST will update the user's streaks
            calcStreak(request.user)

            moodSerializer = MoodSerializer(data = data)
            if moodSerializer.is_valid(): #If the data is valid and creates a valid object, will save the data to the SQLite database using the moods Model
                moodSerializer.save()

                #Recalculates users percentile score in case it changes after their streak changes or other users have changed the score
                check_bool = calcPercentile(request.user)

                #Collects current streak data now that it will no longer be edited. Pops data into streakData incase what is presented needs to be changed
                curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
                streakSerializer = StreakSerializer(curr_Streak_temp)
                streakData = streakSerializer.data
                if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                    streakData.pop('percentile')

                return Response({'moods': moodSerializer.data, 'streak': streakData }, status=status.HTTP_201_CREATED) #Then returns a response signifying that the data was added
            return Response(moodSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #Otherwise returns a bad request

        elif request.method == 'GET': #Whenever a user visits /mood/ or calls for a GET will filter for moods based on user ordered by date
            moods = Moods.objects.filter(user = request.user).order_by('-date')
            moodSerializer = MoodSerializer(moods, many = True)

            #Rechecks if users percentile has changed in other users streaks have changed
            check_bool = calcPercentile(request.user)
            curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
            streakSerializer = StreakSerializer(curr_Streak_temp)
            streakData = streakSerializer.data
            if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                streakData.pop('percentile')

            return Response({'moods': moodSerializer.data, 'streak': streakData})
    else:
        return redirect('/signin/')
'''
@permission_classes((permissions.AllowAny,))
class MoodList(generics.ListCreateAPIView):

    queryset = Moods.objects.all().order_by('-date')
    serializer_class = MoodSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
    filter_fields = ('date',)
    permission_classes = (MoodObjectPermissions, permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, format = None):
        if(request.user.username != ''):
            data = request.data
            #data['user'] = request.user.username #Adds username to collected data

            #Checks if this new POST will update the user's streaks
            calcStreak(request.user)

            moodSerializer = MoodSerializer(data = data)
            if moodSerializer.is_valid() and data['user'] == request.user.username:
                #If the data is valid and creates a valid object, and is under the right username, will save the data to the SQLite database using the moods Model
                moodSerializer.save()

                #Recalculates users percentile score in case it changes after their streak changes or other users have changed the score
                check_bool = calcPercentile(request.user)

                #Collects current streak data now that it will no longer be edited. Pops data into streakData incase what is presented needs to be changed
                curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
                streakSerializer = StreakSerializer(curr_Streak_temp)
                streakData = streakSerializer.data
                if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                    streakData.pop('percentile')

                return Response({'moods': moodSerializer.data, 'streak': streakData }, status=status.HTTP_201_CREATED) #Then returns a response signifying that the data was added
            return Response(moodSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #Otherwise returns a bad request
        else:
            return redirect('/signin/')

    def get(self, request, format = None):
        if(request.user.username != ''):
            moods = Moods.objects.filter(user = request.user).order_by('-date')
            moodSerializer = MoodSerializer(moods, many = True)

            #Rechecks if users percentile has changed in other users streaks have changed
            check_bool = calcPercentile(request.user)
            curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
            streakSerializer = StreakSerializer(curr_Streak_temp)
            streakData = streakSerializer.data
            if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                streakData.pop('percentile')

            return Response({'moods': moodSerializer.data, 'streak': streakData})
        else:
            return redirect('/signin/')

#A secondary mood view class utilizaed for detailed calls to GET
class MoodDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Moods.objects.all().order_by('-date')
    serializer_class = MoodSerializer

    #Therefore it only has the GET method
    def get(self, request, *args, **kwargs):
        #print(kwargs)
        #Checks that a user is logged in
        if(request.user.username != ""):
            option = kwargs.get('point')
            if(option==None): #If no word was input before the date it is assumed the user has given 2 dates. That is the only way this should be called then.
                yearS = kwargs['yearS']
                monthS = kwargs['monthS']
                dayS = kwargs['dayS']

                #Attempts to create a datetime with the given integers
                try:
                    datetimeStart = datetime.datetime(yearS, monthS, dayS)
                except: #Will redirect to the main mood endpoint if this fails
                    return(redirect('/mood/'))

                yearE = kwargs['yearE']
                monthE = kwargs['monthE']
                dayE = kwargs['dayE']


                try:
                    datetimeEnd = datetime.datetime(yearE, monthE, dayE)
                except:
                    return(redirect('/mood/'))

                #Filters between the first and second given date
                moods = self.queryset.filter(user = request.user, date__gte = datetimeStart, date__lte = datetimeEnd)
                moodSerializer = MoodSerializer(moods, many = True)

                #Rechecks if users percentile has changed in other users streaks have changed
                check_bool = calcPercentile(request.user)
                curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
                streakSerializer = StreakSerializer(curr_Streak_temp)
                streakData = streakSerializer.data
                if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                    streakData.pop('percentile')

                return Response({'moods': moodSerializer.data, 'streak': streakData})

            elif(option == 'start' or option == 'end'): #Checks that a user input start or end
                year = kwargs['year']
                month = kwargs['month']
                day = kwargs['day']

                try:
                    datetimePoint = datetime.datetime(year, month, day)
                except:
                    return redirect('/mood/')

                moods = self.queryset

                if(option == 'start'): #Filters based on whether user input start or end
                    moods = moods.filter(user = request.user, date__gte = datetimePoint)
                else:
                    moods = moods.filter(user = request.user, date__lte = datetimePoint)

                moodSerializer = MoodSerializer(moods, many = True)

                #Rechecks if users percentile has changed in other users streaks have changed
                check_bool = calcPercentile(request.user)
                curr_Streak_temp = Streaks.objects.filter(user = request.user)[0]
                streakSerializer = StreakSerializer(curr_Streak_temp)
                streakData = streakSerializer.data
                if(check_bool): #If the percentile is below 50%, should remove percentile from the data that will be presented
                    streakData.pop('percentile')

                return Response({'moods': moodSerializer.data, 'streak': streakData})

            else: #If something other than start or end was input after mood redirects back to mood
                return redirect('/mood/')
        else: #Redirects to signin if not logged in
            return redirect('signin/')


#@permission_classes((permissions.AllowAny,))
class CorrelationList(generics.ListCreateAPIView):
    queryset = Correlations.objects.all()
    serializer_class = CorrelationSerializer

    def get(self, request, format = None):
        calcCorrelations()
        correlations = Correlations.objects.all()
        correlationSerializer = CorrelationSerializer(correlations, many = True)

        return Response(correlationSerializer.data)



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
                #If succesful will create and save user account
                new_user = User.objects.create_user(user_tmp, email_tmp, password_tmp)
                new_user.save()

                #Create their connected streak model and save it
                new_streak = Streaks(user = new_user)
                new_streak.save()

                #Then it logs the user in and redirects them to the mood endpoing
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