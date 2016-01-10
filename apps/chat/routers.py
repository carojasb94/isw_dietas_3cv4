from swampdragon import route_handler
from swampdragon.message_format import format_message
from swampdragon.permissions import LoginRequired
from swampdragon.pubsub_providers.model_channel_builder import make_channels
from swampdragon.route_handler import ModelPubRouter, BaseRouter, CHANNEL_DATA_SUBSCRIBE
from .models import Notification, Mensaje
from .serializers import NotificationSerializer, MensajeSerializer

'''
class NotificationRouter(ModelPubRouter):
    valid_verbs = ['subscribe','get_single']
    #valid_verbs = ['subscribe']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer

    def get_object(self, **kwargs):
        print(self)
        print(kwargs)
        pass
'''
class NotificacionesRouter(ModelPubRouter):
    valid_verbs = ['get_list','get_single', 'create', 'update', 'delete', 'subscribe', 'unsubscribe', 'molestar_usuario']
    #Nombre del router
    route_name = 'mensajes_eds'
    model = Mensaje
    serializer_class = MensajeSerializer

    #FUNCION CUSTOM PARA PUBLICAR
    def custom(self, value):
        print("CUSTOM___")
        print(self)
        print(vars(self))
        #self.publish(['notificacion|*'], {'hello': 'world'})
        self.publish(['notificaciones'], {'hello': 'world'})

    def get_query_set(self, **kwargs):
        print("get_query_set_________________-")
        #print(self)
        #print(kwargs)
        return self.model.objects.filter(user=self.connection.user)

    def get_object(self, **kwargs):
        print("get_object____________________")
        #print(self)
        #print(kwargs)
        #return self.model.objects.get(user=self.connection.user , pk=kwargs['pk'])
        return self.model.objects.get(user=self.connection.user , pk=kwargs['pk'])

    # FUNCION ESPECIAL PARA PUBLICAR EN UN CANAL EN ESPECIFICO
    def get_subscription_channels(self, **kwargs):

        print("GET_SUBSCRIPTION_CHANNELS____________________")
        if self.connection.user is None:
            print("Usuario no logueado")
            return ['anonimo']
            #return self.model.objects.get(user=self.connection.user, pk=kwargs['pk'])
        else:
            return ['notificaciones']
            #return ['usuario']

    def subscribe(self, **kwargs):
        client_channel = kwargs.pop('channel')
        server_channels = make_channels(self.serializer_class, self.include_related, self.get_subscription_contexts(**kwargs))
        data = self.serializer_class.get_object_map(self.include_related)
        channel_setup = self.make_channel_data(client_channel, server_channels, CHANNEL_DATA_SUBSCRIBE)
        self.send(
            data=data,
            channel_setup=channel_setup,
            **kwargs
        )
        self.connection.pub_sub.subscribe(server_channels, self.connection)

        print("SUBSCRIBE_____")
        print("KWARGS")
        print(kwargs)

        print("SELF_SERIALIZER_CLASS")
        print(vars(self.serializer_class))
        print("SELF._INCLUDE_RELATED")
        print(self.include_related)

        print("CLIENT_CHANNEL")
        print(client_channel)
        print("SERVER_CHANNELS")
        print(server_channels)
        print("DATA")
        print(data)
        print("CHANNEL_SETUP")
        print(channel_setup)
        print("SELF AL FINAL")
        print(vars(self.connection))

    def get_subscription_contexts(self, **kwargs):
        #broadcast_sys_info()
        print("get_subscription_contexts______________________")
        print(""+str(vars(self)))
        print("kwargs__GSC")
        print(kwargs)
        #print(kwargs[])
        print("vars(self.connection)__")
        print(vars(self.connection))
        contexto = dict()
        contexto['user__id'] = self.connection.user.pk
        print("contexto = ",contexto)
        return contexto

    def get_client_context(self, verb, **kwargs):
        print("get_client_context________________________")
        return {'id__': self.connection.user.pk}

    def send(self, data, channel_setup=None, **kwargs):
        print("metodo send______________________-")
        self.context['state'] = 'success'
        if 'verb' in self.context:
            client_context = self.get_client_context(self.context['verb'], **kwargs)
            self._update_client_context(client_context)
            print("Client_context : "+str(client_context))

        message = format_message(data=data, context=self.context, channel_setup=channel_setup)
        #print("se enviara el mensaje "+str(message))
        self.connection.send(message)
        print("se ENVIO mensaje "+str(message))


route_handler.register(NotificacionesRouter)

