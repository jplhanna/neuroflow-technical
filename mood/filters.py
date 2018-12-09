import django_filters
from .models import Moods

class MoodFilter(django_filters.FilterSet):
    class Meta:
        model = Moods
        fields = { 'date' : ['lte', 'gte'] }