from django.db import models


class BlackListedSite(models.Model):
    """
    Not implemented yet, this should blacklist any website that's not unscrapable by this script to avoid performance
    issues.
    """
    url = models.URLField()


class Client(models.Model):
    """
    Not implemented yet, Represents a client for the notification system.
    """
    channel_name = models.CharField(max_length=255)
