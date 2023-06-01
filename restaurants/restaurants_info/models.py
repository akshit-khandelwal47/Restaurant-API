from django.db import models

# Create your models here.

class storestatus(models.Model):
    store_id = models.IntegerField()
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField()