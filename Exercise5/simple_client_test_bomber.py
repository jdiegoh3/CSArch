#!/usr/bin/env python
import pika
import uuid
import threading
import sys

class AddServerClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='add',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def thread_function():
    add_rpc = AddServerClient()

    print(" [x] Requesting add")
    response = add_rpc.call("+|1|2")
    print(" [.] Got %r" % response)
    sys.exit()

if __name__ == "__main__":
    threads = 1000000
    for i in range(0, threads):
        temp_thread = threading.Thread(target=thread_function)
        temp_thread.start()