import logging
import os
import socket

from confluent_kafka import Producer
from logmaster.core.config import EnvVars

_logger = logging.getLogger(__name__)


def delivery_callback(error, msg):
    if error:
        _logger.error("Message delivery failed: %s", error)
        return
    _logger.info(
        "Produced event to topic [%s]: key=[%s], value=[%s]",
        msg.topic(), msg.key(), msg.value().decode('utf-8')
    )


class ProducerClient:

    def __init__(self, servers: str = None):

        self.__producer = Producer(
            {
                'bootstrap.servers': servers or os.environ[EnvVars.KAFKA_BOOTSTRAP_SERVERS],
                'client.id': socket.gethostname()
            }
        )

    @property
    def producer(self):
        return self.__producer

    def produce(self, topic: str, value: str | bytes = None):
        self.producer.produce(topic=topic, value=value, on_delivery=delivery_callback)

    def produce_and_poll(self, topic: str, value: str | bytes = None):
        self.produce(topic=topic, value=value)
        self.producer.poll(1)
