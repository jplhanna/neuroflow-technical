# neuroflow-technical
A technical REST project for Collecting, tracking, and presenting users Mood, and the data related to it.
After installing the necessary libraries, the server can be run with python manage.py runserver (Server IP):(Server Port)

The website includes the endpoints:
mood
signup
signin
signout
mood_streak_correlation

Users must make a an account in signup before being able to POST a mood.

In the mood endpoint users can get all moods they have posted, including filtering by days using:

They are also given information about their streaks, aka the number of days in a row they have posted a mood.
currStreak standing for the current streak they have going, and currStart for the day that streak started.
maxStreak standing for the largest streak they've had during the users account life time.
maxStart and maxEnd representing the start and end of this streak.
If the users maxStreak places in the 50% or above percentile in length vs all users, they are presented this percentage.

Users can also filter which moods they see with dates.
If they wish to see all moods starting from a certain day they may add /start/yyyy/mm/dd, to the end of the /mood/ endpoint
Where yyyy represents the full year in integers they want to start from, mm is the full month in integers, and dd is the full day in integers.
If they wish to see all moods before and including a certain day they may add /end/yyyy/mm/dd, to the end of the /mood/ endpoint
Or if they wish to see all moods between 2 days they may add /yyyy/mm/dd/yyyy/mm/dd, to the end of the /mood/ endpoint.
The first set of yyyy/mm/dd is the starting date, and the second is the ending date.
If a user inputs an invalid date, or a word other than start or end, they will be redirected back to mood.

In the mood_streak_correlation endpoint all users are given every users correlations of their moods vs streak length and consistency.
First, showing their over all avg mood vs percent consistency of mood posting.
Consistency represent their longest streak vs their account life time.
Second, they are shown their avg mood during their max streak, vs how long that streak was.