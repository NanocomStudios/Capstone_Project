import pika
import json
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

def publish(queue_name: str, message: dict):
    """Publish message to RabbitMQ"""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST)
        )
        channel = connection.channel()
        
        channel.queue_declare(queue=queue_name, durable=True)
        
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
        connection.close()
    except Exception as e:
        print(f"Failed to publish: {e}")

def consume(queue_name: str, callback):
    """Consume messages from RabbitMQ"""

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        while True:
            
            def on_message(ch, method, properties, body):
                message = json.loads(body)
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=on_message)
            
            print(f"Waiting for messages in {queue_name}...")
            channel.start_consuming()
    except Exception as e:
        print(f"Failed to consume: {e}")