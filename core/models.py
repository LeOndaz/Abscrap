from django.db import models
from django.db.models.signals import post_save


class TimestampedModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BlackListedSite(TimestampedModelMixin, models.Model):
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


class Notification(TimestampedModelMixin, models.Model):
    """
    TL;DR: This is a global server notification.
    Represents a simple notification to people subscribed to 'notifications' channel group.
    This notification is sent upon creation, this removes the ability to create draft notifications or targets users.
    This is a design choice because this site has no authentication system.
    """
    content = models.TextField()

    def __str__(self):
        """
        Shorten the notification as "You've a ...... cation" if it's longer than 30 (reprlib.repr default)
        """
        import reprlib
        return reprlib.repr(self.content)[1: -2]

    @staticmethod
    def post_create(sender, instance, created, *args, **kwargs):
        """
        A signal to send the serialized notification after creation to 'notifications' channel group.
        """
        from asgiref.sync import async_to_sync
        from channels.layers import get_channel_layer
        from core.api.serializers import NotificationSerializer

        if created:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)(
                'notifications',
                {
                    "type": "handle.notification",
                    "notification":
                        NotificationSerializer(instance).data
                }
            )


post_save.connect(Notification.post_create, sender=Notification)
