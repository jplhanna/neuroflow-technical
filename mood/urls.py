from django.urls import path
from .views import *
from .filters import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('mood/', MoodList.as_view()),
    path('mood/<str:point>/<int:year>/<int:month>/<int:day>/', MoodDetail.as_view()),
    path('mood/<int:yearS>/<int:monthS>/<int:dayS>/<int:yearE>/<int:monthE>/<int:dayE>/', MoodDetail.as_view()),
    path('signup/', signUp),
    path('signin/', signIn),
    path('signout/', signOut),
    path('mood_streak_correlation/', CorrelationList.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)