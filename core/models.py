from django.db import models


class BlackListedSite(models.Model):
    url = models.URLField()


class Client(models.Model):
    channel_name = models.CharField(max_length=255)
