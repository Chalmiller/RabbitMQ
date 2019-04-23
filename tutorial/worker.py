import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)
channel.queue_bind(exchange='logs',
                   queue=result.method.queue)
# channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='hello',
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CRTL+C')

channel.start_consuming()