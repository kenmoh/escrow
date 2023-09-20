import pika
from pika.exceptions import ChannelWrongStateError, ConnectionWrongStateError


URL = 'amqps://grljjhae:M3tmfWEgI9yIfNR7-ad2QJE1rBtlT65F@moose.rmq.cloudamqp.com/grljjhae'


def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.URLParameters(URL))
    channel = connection.channel()
    channel.queue_declare(queue='wallet')
    return connection, channel


def close_rabbitmq_channel(connection, channel):
    try:
        channel.close()
    except (ChannelWrongStateError, ConnectionWrongStateError):
        pass


