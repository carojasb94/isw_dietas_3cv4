from swampdragon.serializers.model_serializer import ModelSerializer

'''
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = 'demo.Notification'
        publish_fields = ['message']
'''

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = 'demo.Notification'
        publish_fields = ['message','verb','user','img']


class MensajeSerializer(ModelSerializer):
    class Meta:
        model = 'chat.Mensaje'
        publish_fields = ['mensaje','remitente','destinatario','fecha']





