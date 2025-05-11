import logging

import requests

from logmaster.client.logger import KafkaLoggingHandler
from logmaster.core.logging import LogFormatter

BACKEND_ROOT_URL = "http://localhost:5050"
BACKEND_URL = BACKEND_ROOT_URL + "/api/v1/"
APP_NAME = "demo-app"


def test_error(_logger):
    try:
        raise Exception("dummy exception")
    except Exception as e:
        _logger.exception(e, exc_info=True, stack_info=True)


def test():

    kafka_handler = KafkaLoggingHandler(id_app=APP_NAME, backend_server=BACKEND_ROOT_URL, app_info={"name": "Demo APP"})

    _logger = logging.getLogger(__name__)
    _logger.addHandler(kafka_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(LogFormatter())
    _logger.addHandler(stream_handler)
    _logger.setLevel(logging.INFO)

    _logger.info("A test [info] message")
    _logger.error("A test [error] message")

    test_error(_logger)


if __name__ == "__main__":
    test()
