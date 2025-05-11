import logging
from logging import Handler, LogRecord
from urllib.parse import urljoin

import requests

from logmaster.core.logging import LogMessage
from logmaster.core.producer.message import LogMessageProducerClient
from logmaster.core.util import Singleton

_logger = logging.getLogger(__name__)


class KafkaLoggingHandler(Handler, metaclass=Singleton):

    def __init__(self, id_app: str, backend_server: str, bootstrap_servers: str = None, app_info: dict[str, str] = None):
        super().__init__()
        _logger.info("Configuring KafkaLoggingHandler...")
        self._producer = LogMessageProducerClient(bootstrap_servers)
        self._id_app = id_app
        self._backend_server = backend_server
        self.__post_init(app_info=app_info)

    def __post_init(self, app_info: dict[str, str] = None):
        if app_info is None:
            self.__validate()
        else:
            self.__create_or_replace_app(app_info)

    def __validate(self):
        response = requests.get(
            urljoin(self._backend_server, f"api/v1/apps/{self._id_app}")
        )
        if response.ok:
            _logger.info("KafkaLoggingHandler configured to talk with app: %s", response.json())
            return
        _logger.error("Unable to get app %s, the server response is: %s", self._id_app, response.json())
        response.raise_for_status()

    def __create_or_replace_app(self, app_info: dict[str, str]):
        response = requests.put(
            urljoin(self._backend_server, f"api/v1/apps/{self._id_app}"),
            json=app_info
        )
        if response.ok:
            _logger.info("KafkaLoggingHandler configured to talk with app: %s", response.json())
            return
        _logger.error("Unable to upsert app %s, the server response is: %s", self._id_app, response.json())
        response.raise_for_status()

    def emit(self, record: LogRecord):
        message_text = self.format(record)
        message = LogMessage.from_log_record(id_app=self._id_app, record=record, message_text=message_text)
        self._producer.produce(message)
