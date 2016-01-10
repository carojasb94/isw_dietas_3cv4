from django.conf import settings
from django.db import models
from django.templatetags.static import static
from swampdragon.models import SelfPublishModel
from .serializers import NotificationSerializer


'''
class Notification(SelfPublishModel, models.Model):
    serializer_class = NotificationSerializer
    message = models.TextField()
'''

class Notification(SelfPublishModel, models.Model):
    serializer_class = NotificationSerializer
    message = models.TextField()
    verb = models.CharField(null=True, default="achieved", max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    img = models.ImageField(default=static('img/frida_30x30.jpg'))


