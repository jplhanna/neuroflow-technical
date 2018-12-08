from .models import *
from django.utils import timezone
import datetime


def calcStreak(user):
    moods = Moods.objects.filter(user = user).order_by('-date')
    if moods.exists():
        last_date = moods[0].date
        if(datetime.timedelta(days = 2) < timezone.now() - last_date >= datetime.timedelta(days = 1)):
            return moods[0].streak + 1
        if(timezone.now() - last_date < datetime.timedelta(days = 1)):
            return moods[0].streak
    return 1        