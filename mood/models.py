from django.db import models


# Create your models here.

class Moods(models.Model):
    #Int score for a users mood, will default to 5 if a number is not input
    moodScore =  models.IntegerField(default = 5)
    #Date that the score was input, models takes care of this, and is not required as a user input
    date = models.DateTimeField(auto_now_add = True)