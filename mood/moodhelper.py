from .models import *
from django.utils import timezone
import datetime
from django.db.models import Avg
from django.contrib.auth.models import User


def findBetween(user, start, end = timezone.now()):
    return Moods.objects.filter(user = user, date__gte = start, date__lte = end)






#Checks if a user needs to update streak data, then updates it
def calcStreak(user):
    #Collects users mood data, and streak model
    moods = Moods.objects.filter(user = user).order_by('-date')
    curr_Streak_Info = Streaks.objects.filter(user = user)[0]
    
    #If the user has POSTed a mood before:
    if moods.exists():
        #Checks if the last time the user POSTed a mood is within 24 and 48 hours
        last_date = moods[0].date
        if(datetime.timedelta(days = 2) < timezone.now() - last_date >= datetime.timedelta(days = 1)):
            #If so, increments the users current streak by 1
            new_Streak = curr_Streak_Info.currStreak + 1
            curr_Streak_Info.currStreak = new_Streak
            
            #If this new streak is greater than their max streak, updates that accordingly
            if(new_Streak > curr_Streak_Info.maxStreak):
                curr_Streak_Info.maxStreak = new_Streak
                curr_Streak_Info.maxStart = curr_Streak_Info.currStart
                curr_Streak_Info.maxEnd = timezone.now()
                
            
        #elif(timezone.now() - last_date < datetime.timedelta(days = 1)):
        #    return moods[0].streak
        
        #Checks if the last time a user POSTed a mood is greater than 48 hours
        elif(timezone.now() - last_date >= datetime.timedelta(days = 2)):
            #If so, resets current streak to 1
            curr_Streak_Info.currStreak = 1
            curr_Streak_Info.currStart = timezone.now()
        #Otherwise the user POSTed on the same day, and the streak shouldn't change
    #If this this the first time a user has POSTed a mood
    else:
        #Sets current streak and max streak to 1
        curr_Streak_Info.currStreak = 1
        curr_Streak_Info.maxStreak = 1
        curr_Streak_Info.currStart = timezone.now()
    curr_Streak_Info.save()
    
#Calculates the percentile that the user's max streak places vs all users
def calcPercentile(user):
    #Collects the users max streak
    curr_Streak_Info = Streaks.objects.filter(user = user)[0]
    personal_max = curr_Streak_Info.maxStreak
    #The total number of users
    all_streaks = Streaks.objects.all().count()
    #And the number of users with a max streak less than the current user
    streaks_LT = Streaks.objects.filter(maxStreak__lte = personal_max).count()
    
    #Calculates the percentile, and updates the users streak value
    percentile = streaks_LT / all_streaks * 100
    curr_Streak_Info.percentile = percentile
    curr_Streak_Info.save()
    
    #Returns whether the value is less than 50% or not
    return percentile < 50
    
    
    
def calcCorrelations():
    for user in User.objects.all():
        avg = Moods.objects.filter(user = user).aggregate(avg = Avg('moodScore')) #Double check filtering this way with Avg
        #print(Moods.objects.filter(user=user))
        #print("avg: ", avg)
        streak = Streaks.objects.filter(user = user)[0]
        startDelta = timezone.now() - user.date_joined
        maxStreak = streak.maxStreak
        consistency = datetime.timedelta(days = maxStreak) / startDelta * 100
        maxStart = streak.maxStart
        maxEnd = streak.maxEnd
        
        maxStreakAvg = Moods.objects.filter( user = user).aggregate(maxAvg = Avg('moodScore', date__lte = maxStart, date__gte = maxEnd))
        #print(Moods.objects.filter( user = user,  date__gte = maxStart, date__lte = maxEnd))
        #print("maxStreakAvg: ", maxStreakAvg)
        correlation_temp = Correlations.objects.filter(user = user)
        if(correlation_temp.exists()):
            corr_update = correlation_temp[0]
            corr_update.avg = avg['avg']
            corr_update.consistency = consistency
            corr_update.maxStreakAvg = maxStreakAvg['maxAvg']
            corr_update.maxStreak = maxStreak
            corr_update.save()
        else:
            new_correlation = Correlations(avg = avg['avg'], consistency = consistency, maxStreakAvg = maxStreakAvg['maxAvg'], maxStreak = maxStreak, user = user)
            new_correlation.save()
    