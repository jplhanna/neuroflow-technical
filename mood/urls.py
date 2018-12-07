from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('mood/', mood_list)
    ]
    
urlpatterns = format_suffix_patterns(urlpatterns)