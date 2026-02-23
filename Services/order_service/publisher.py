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