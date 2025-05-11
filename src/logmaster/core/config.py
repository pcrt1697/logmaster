import os
from enum import StrEnum


class MongoConfig(StrEnum):
    DB_NAME = 'logmaster'
    COLLECTION_MSG = 'messages'


class EnvVars(StrEnum):
    KAFKA_CONNECT_URL = 'LOGMASTER_KAFKA_CONNECT_URL'
    KAFKA_BOOTSTRAP_SERVERS = 'LOGMASTER_KAFKA_BOOTSTRAP_SERVERS'
    BACKEND_PORT = 'LOGMASTER_BACKEND_PORT'
    DB_URL = 'LOGMASTER_MONGO_URL'

    def get_value(self):
        # noinspection PyTypeChecker
        return os.environ.get(self.value)


class Topics(StrEnum):
    MONGO_SINK = 'logmaster-mongo-sink'
