from django.db import models


class LogData(models.Model):
    ip = models.CharField(max_length=15)
    date = models.DateTimeField()
    http_method = models.CharField(max_length=8)
    url = models.TextField()
    response_code = models.CharField(max_length=3)
    response_size = models.IntegerField()


