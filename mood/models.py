from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#__str__ is used for easy database access in admin mode


class Moods(models.Model):
    #Int score for a user's mood, will default to 5 if a number is not input
    moodScore =  models.IntegerField(default = 5)
    #Date that the score was input, models takes care of this, and is not required as a user input
    date = models.DateTimeField(auto_now_add = True)
    #User foreignkey to connect users to their mood scores
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    
    def __str__(self):
        return  self.user.username + ": (" + str(self.date) + ", " + str(self.moodScore) + ")"

#Model for tracking a Users streaks and streak related information
class Streaks(models.Model):
    #Int value for user's current streak, defaults to 0
    currStreak = models.IntegerField(default = 0)
    
    #currStart = models.DateTimeField(default = timezone.now())
    
    #Int value for user's lifetime max streak, defaults to 0
    maxStreak = models.IntegerField(default = 0)
    
    #maxStart = models.DateTimeField(default = timezone.now())
    
    #maxEnd = models.DateTimeField(defualt = timezone.now())
    
    #Float value of percentile placement of user's max streak vs all users
    percentile = models.FloatField(default = 0.0)
    #User foreignkey to connect users to their mood scores
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.user.username + ": (" + str(self.maxStreak) + ", " + str(self.currStreak) + ")"