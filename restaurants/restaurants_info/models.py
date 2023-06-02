from django.db import models

# Create your models here.

class storestatus(models.Model):
    store_id = models.IntegerField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField()

class TimeZone(models.Model):
    store_id = models.IntegerField()
    timezone_str = models.CharField(max_length=30)

class MenuHours(models.Model):
    store_id = models.IntegerField()
    week_day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()