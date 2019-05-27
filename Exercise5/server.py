#!/usr/bin/env python
import pika
import lib.protocol_utils as protocol_utils

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='add')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    data = protocol_utils.MessageHandler(body).message_loads()
    if data and data[0] == "+":
        try:
            response = protocol_utils.MessageResponseBuilder(False, str(float(data[1]) + float(data[2])))
        except ValueError:
            response = protocol_utils.MessageResponseBuilder(True, "The operands requires to be numbers")
    else:
        response = protocol_utils.MessageResponseBuilder(True, "Invalid operation")
    
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=str(response.get_message()))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue='add', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()