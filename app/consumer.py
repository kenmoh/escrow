import pika
import json

# URL = 'amqps://fzrzebvc:UlR8AmDkg6ecyJ7Eqm21Z6nDtPwQTjkU@moose.rmq.cloudamqp.com/fzrzebvc'
URL = 'amqps://grljjhae:M3tmfWEgI9yIfNR7-ad2QJE1rBtlT65F@moose.rmq.cloudamqp.com/grljjhae'
# URL = 'localhost'
connection = pika.BlockingConnection(pika.URLParameters(URL))

channel = connection.channel()

channel.queue_declare(queue='wallet')


def callback(ch, method, properties, body):

    data = json.loads(body)
    if properties.content_type == 'get_order':
        print(data)

    if properties.content_type == 'get_product':
        print(data)


channel.basic_consume(queue='wallet',
                      auto_ack=True,
                      on_message_callback=callback)

print(channel.is_open)
print(' [*] Waiting for messages. To exit press CTRL+C')
print(channel.is_open)
channel.start_consuming()
