from django.db import models
import django
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


class Report(models.Model):
    report_id = models.CharField(primary_key=True, max_length=16)
    status = models.CharField(max_length=50)
    data = models.TextField(null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    completed_at = models.DateTimeField(null=True)

