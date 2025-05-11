import json
import logging
from urllib.parse import urljoin

import requests

from logmaster.core.config import EnvVars, Topics, MongoConfig

_logger = logging.getLogger(__name__)


class KafkaConnectClient:

    __connector_name = 'mongo-sink'

    def __init__(self, url: str = None):
        self.__url = url or EnvVars.KAFKA_CONNECT_URL.get_value()
        if not self.__url:
            raise EnvironmentError(
                f"Missing client configuration: cannot set the url for {self.__class__}. "
                f"Either provide an URL or set the variable [{EnvVars.KAFKA_CONNECT_URL.value}]."
            )

    @property
    def connector_name(self):
        return self.__connector_name

    @property
    def connectors_url(self):
        return urljoin(self.__url, 'connectors')

    def register_sink_connector(self):
        request_body = {
            "name": self.connector_name,
            "config": {
                "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
                "tasks.max": "1",
                "topics": Topics.MONGO_SINK.value,
                "connection.uri": EnvVars.DB_URL.get_value(),
                "database": MongoConfig.DB_NAME.value,
                "collection": MongoConfig.COLLECTION_MSG.value,
                "key.converter": "org.apache.kafka.connect.storage.StringConverter",
                "value.converter": "org.apache.kafka.connect.json.JsonConverter",
                "value.converter.schemas.enable": "false",
                "transforms": "TimestampConverter",
                "transforms.TimestampConverter.type": "org.apache.kafka.connect.transforms.TimestampConverter$Value",
                "transforms.TimestampConverter.field": "timestamp",
                "transforms.TimestampConverter.format": "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
                "transforms.TimestampConverter.target.type": "Timestamp"
            }
        }
        response = requests.post(
            url=self.connectors_url,
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        _logger.info("Connector creation response: %s", json.dumps(response.json(), indent=4))
        response.raise_for_status()
        _logger.info("Created topic [%s] for sink connector [%s]", Topics.MONGO_SINK, self.connector_name)

    def delete_connector(self):
        url = urljoin(self.__url, f'connectors/{self.connector_name}')
        response = requests.delete(url=url)
        response.raise_for_status()
        _logger.info("Deleted connector: %s", Topics.MONGO_SINK)

    @property
    def is_running(self):
        url = urljoin(self.__url, f'connectors/{self.connector_name}/status')
        response = requests.get(url=url)
        if response.status_code == 404:
            return False
        else:
            response.raise_for_status()
        return response.json().get("connector", {}).get("state") == "RUNNING"
