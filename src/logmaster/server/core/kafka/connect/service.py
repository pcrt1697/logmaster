import logging

from logmaster.server.core.kafka.connect.client import KafkaConnectClient

_logger = logging.getLogger(__name__)


def initialize_connector(force: bool = False):
    client = KafkaConnectClient()
    if force or not client.is_running:
        client.delete_connector()
        client.register_sink_connector()
        _logger.info("Sink connector initialized successfully")
