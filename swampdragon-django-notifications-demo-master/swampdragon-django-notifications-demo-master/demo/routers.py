from swampdragon import route_handler
from swampdragon.message_format import format_message
from swampdragon.permissions import LoginRequired
from swampdragon.route_handler import ModelPubRouter, BaseRouter
from .models import Notification
from .serializers import NotificationSerializer

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

from swampdragon.route_handler import ModelRouter
class TodoItemRouter(ModelRouter):
    valid_verbs = ['subscribe']
    route_name = 'todo-item'
    serializer_class = NotificationSerializer
    model = Notification
    permission_classes = [LoginRequired()]

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(user__id=kwargs['list_id'])

#class NotificationRouter(ModelPubRouter):
#class NotificationRouter(ModelRouter):
class NotificationRouter(ModelPubRouter):
    valid_verbs = ['subscribe']
    #valid_verbs = ['subscribe','get_single']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer

    def get_query_set(self, **kwargs):
        print("get_query_set_________________-")
        print(self)
        print(kwargs)
        return self.model.objects.filter(user=self.connection.user)

    def get_object(self, **kwargs):
        print("get_object____________________")
        print(self)
        print(kwargs)
        return self.model.objects.get(user=self.connection.user, pk=kwargs['pk'])

    def get_subscription_contexts(self, **kwargs):
        try:
            print("get_subscription_contexts______________________")
            print(self)
            print(""+str(vars(self)))
            print("conection.sesion "+str(vars(self.connection.session)))
            print("conection.session_store,conection.pub_sub._subscriber "+str(vars(self.connection.session_store.connection.pub_sub._subscriber )))
            print("self.conection.user "+ str(self.connection.user))
        except Exception as e:
            print(e)
        return {'user__id': self.connection.user.pk}


    def get_client_context(self, verb, **kwargs):
        print("get_client_context________________________")
        print(self)
        print(verb)
        print(kwargs)
        print("self "+str(vars(self)))
        print("conection "+str(vars(self.connection)))
        print("conection.sesion "+str(vars(self.connection.session)))
        print("conection.user "+str(self.connection.user))
        print("verb "+verb)
        return {'user__id': self.connection.user.pk}

    def send(self, data, channel_setup=None, **kwargs):
        print("metodo send______________________-")
        self.context['state'] = 'success'
        if 'verb' in self.context:
            client_context = self.get_client_context(self.context['verb'], **kwargs)
            self._update_client_context(client_context)
            print("Client_context : "+str(client_context))

        message = format_message(data=data, context=self.context, channel_setup=channel_setup)
        print("se enviara el mensaje "+str(message))
        self.connection.send(message)





class NotificationRouter_2(BaseRouter):
    route_name = 'call-notifications'

    def get_subscription_channels(self,**kwargs):
        channel = 'user_{}'.format(self.connection.user.pk)  # This is depending on swampdragon-auth
        return

route_handler.register(NotificationRouter)
