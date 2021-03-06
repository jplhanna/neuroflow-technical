# Generated by Django 2.1.4 on 2018-12-09 19:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mood', '0007_streaks_percentile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correlations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg', models.FloatField(default=0.0)),
                ('consistency', models.FloatField(default=100.0)),
                ('maxStreakAvg', models.FloatField(default=0.0)),
                ('maxStreak', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='streaks',
            name='currStart',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 9, 19, 30, 4, 868124, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='streaks',
            name='maxEnd',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 9, 19, 30, 4, 868232, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='streaks',
            name='maxStart',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 9, 19, 30, 4, 868184, tzinfo=utc)),
        ),
    ]
