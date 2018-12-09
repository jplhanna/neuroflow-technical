from django.urls import path
from .views import *
from .filters import *
from rest_framework.urlpatterns import format_suffix_patterns
from django_filters.views import FilterView

urlpatterns = [
    path('mood/', MoodList.as_view()),
    path('mood/', FilterView.as_view(filterset_class = MoodFilter)),
    path('signup/', signUp),
    path('signin/', signIn),
    path('signout/', signOut),
    path('mood_streak_correlation/', CorrelationList.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)