from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Moods(models.Model):
    #Int score for a users mood, will default to 5 if a number is not input
    moodScore =  models.IntegerField(default = 5)
    #Date that the score was input, models takes care of this, and is not required as a user input
    date = models.DateTimeField(auto_now_add = True)
    #User foreignkey to connect users to their mood scores
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    streak = models.IntegerField(default = 1) #In each mood model to allow for tracking all max streaks
    
    def __str__(self):
        return  self.user.username + ": (" + str(self.date) + ", " + str(self.moodScore) + ")"