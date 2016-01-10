from swampdragon.pubsub_providers.data_publisher import publish_data

__author__ = 'metallica'



def notify_user_of_a_call(user_id):
    channel = 'user_{}'.format(user_id)
    publish_data(channel=channel, {'message': 'Incoming call'})


