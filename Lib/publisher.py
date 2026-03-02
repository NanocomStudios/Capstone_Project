import pika
import json
import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")

def publish(queue_name: str, message: dict):
    """Publish message to RabbitMQ (direct, single consumer)"""
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
    """Consume messages from RabbitMQ (direct, single consumer)"""

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


# ── Fanout helpers ────────────────────────────────────────────────────────────
# Use these when multiple independent services each need a copy of the same
# event (e.g. wms_order_shipped → CMS adapter AND delivery service).

def publish_fanout(exchange_name: str, message: dict):
    """Broadcast a message to every service subscribed to this exchange."""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type="fanout", durable=True)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key="",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        connection.close()
    except Exception as e:
        print(f"Failed to publish_fanout to {exchange_name}: {e}")


def consume_fanout(exchange_name: str, callback):
    """Receive every message from a fanout exchange (one exclusive queue per consumer)."""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type="fanout", durable=True)

        # Exclusive, auto-delete queue — unique per running consumer instance
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        print(f"Subscribed to fanout exchange '{exchange_name}' on queue '{queue_name}'...")
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to consume_fanout from {exchange_name}: {e}")