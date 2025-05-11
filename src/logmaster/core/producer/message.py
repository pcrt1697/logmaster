import logging

from logmaster.core.logging import LogMessage
from logmaster.core.producer.client import ProducerClient
from logmaster.core.config import Topics
from logmaster.core.util import Singleton

_logger = logging.getLogger(__name__)


class LogMessageProducerClient(metaclass=Singleton):

    def __init__(self, servers: str = None):
        self._client = ProducerClient(servers)

    def produce(self, log_message: LogMessage):
        message = log_message.model_dump_json()
        self._client.produce_and_poll(topic=Topics.MONGO_SINK.value, value=message)
        _logger.info("Message produced: %s", message)
