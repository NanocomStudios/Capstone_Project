import json
import threading
from typing import Callable, Any, Optional

import pika

# Exchange used to broadcast delivery-status changes to other services
DELIVERY_UPDATES_EXCHANGE = "delivery_updates"

# Queue this service consumes to receive new order-assignment events
DELIVERY_ASSIGNMENTS_QUEUE = "delivery_assignments"


class DeliveryRabbitMQ:
    """
    Handles all RabbitMQ interactions for the Delivery Service.

    Responsibilities:
        - Publish delivery-status updates (delivered / failed / route_calculated)
          to the 'delivery_updates' fanout exchange so interested consumers
          (e.g. Client Portal, CMS) can react.
        - Consume 'delivery_assignments' queue to receive new assignments pushed
          by the Order Service without tight coupling.
    """

    def __init__(self, host: str = "localhost"):
        self.host = host
        self._channel: Any = None
        self._connect()

    # ------------------------------------------------------------------ #
    #  Internal connection helper                                          #
    # ------------------------------------------------------------------ #

    def _connect(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            channel = connection.channel()

            # Fanout exchange — every bound consumer gets every update
            channel.exchange_declare(
                exchange=DELIVERY_UPDATES_EXCHANGE,
                exchange_type="fanout",
                durable=True,
            )

            # Inbound queue for driver-assignment messages from Order Service
            channel.queue_declare(
                queue=DELIVERY_ASSIGNMENTS_QUEUE,
                durable=True,
            )

            self._channel = channel
            print(f"[RabbitMQ] Connected to {self.host}")
        except Exception as exc:
            print(f"[RabbitMQ] Could not connect: {exc}")
            self._channel = None

    # ------------------------------------------------------------------ #
    #  Publisher                                                           #
    # ------------------------------------------------------------------ #

    def publish_delivery_update(
        self,
        entity_id: str,
        event: str,
        data: Optional[Any] = None,
    ):
        """
        Publish a delivery update to the fanout exchange.

        Args:
            entity_id: delivery_id or driver_id relevant to the event.
            event:     Event name, e.g. 'delivered', 'failed', 'route_calculated'.
            data:      Optional payload dict to attach to the message.
        """
        if self._channel is None:
            print("[RabbitMQ] Not connected — skipping publish")
            return

        message = json.dumps(
            {"entity_id": entity_id, "event": event, "data": data}
        )
        try:
            self._channel.basic_publish(
                exchange=DELIVERY_UPDATES_EXCHANGE,
                routing_key="",          # fanout ignores routing key
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2      # make message persistent
                ),
            )
            print(f"[RabbitMQ] Published '{event}' for entity '{entity_id}'")
        except Exception as exc:
            print(f"[RabbitMQ] Publish failed: {exc}")

    # ------------------------------------------------------------------ #
    #  Consumer                                                            #
    # ------------------------------------------------------------------ #

    def start_assignment_listener(self, callback: Callable[[dict], None]):
        """
        Start a daemon thread that consumes the delivery_assignments queue.

        When a message arrives the *callback* is called with the parsed dict.
        The callback is responsible for persisting the assignment to the DB.

        Args:
            callback: fn(data: dict) called for each incoming assignment message.
        """

        def _listen():
            try:
                conn = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host)
                )
                ch = conn.channel()
                ch.queue_declare(queue=DELIVERY_ASSIGNMENTS_QUEUE, durable=True)
                ch.basic_qos(prefetch_count=1)

                def _on_message(channel, method, _properties, body):
                    try:
                        data = json.loads(body)
                        callback(data)
                        channel.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as exc:
                        print(f"[RabbitMQ] Error handling message: {exc}")
                        channel.basic_nack(delivery_tag=method.delivery_tag)

                ch.basic_consume(
                    queue=DELIVERY_ASSIGNMENTS_QUEUE,
                    on_message_callback=_on_message,
                )
                print("[RabbitMQ] Waiting for assignment messages…")
                ch.start_consuming()
            except Exception as exc:
                print(f"[RabbitMQ] Listener stopped: {exc}")

        thread = threading.Thread(target=_listen, daemon=True, name="mq-listener")
        thread.start()
