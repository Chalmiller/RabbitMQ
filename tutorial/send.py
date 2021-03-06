#!/usr/bin/env python

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(exclusive=True)

channel.queue_bind(exchange='logs',
                   queue=result.method.queue)

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
# channel.queue_declare(queue='task_queue', durable=True)

message = ''.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='logs',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2)
                      )

print("[x] Sent %r" % message)

connection.close()
