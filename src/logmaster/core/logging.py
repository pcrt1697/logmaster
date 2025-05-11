import logging
from datetime import datetime
from enum import StrEnum, IntEnum
from logging import LogRecord
from typing import Optional

from pydantic import BaseModel, field_serializer, Field, field_validator

from logmaster.core.util import SYSTEM_TZ


LINE_FORMAT = "[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)d] - %(message)s"


class LogFormatter(logging.Formatter):

    # thanks to https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output/56944256#56944256
    COLORS = {
        logging.DEBUG: '\x1b[36m',  # gray
        logging.INFO: '\x1b[38;20m',  # blue
        logging.WARNING: '\x1b[33;20m',  # yellow
        logging.ERROR: '\x1b[31;20m',  # red
        logging.CRITICAL: '\x1b[31;1m'  # bold red
    }

    def __init__(self):
        super().__init__(fmt=LINE_FORMAT)

    def formatMessage(self, record):
        # the literal is used to reset the format
        log_fmt = self.COLORS.get(record.levelno) + LINE_FORMAT + '\x1b[0m'
        formatter = logging.Formatter(log_fmt)
        return formatter.formatMessage(record)


class LogLevel(IntEnum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name.upper()]
        except KeyError | AttributeError:
            # catch KeyError to manage invalid value and AttributeError for null pointer
            return cls._missing_(name)


class LogLevelName(StrEnum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    @classmethod
    def from_level(cls, value: LogLevel):
        return cls(value.name)

    @property
    def level(self):
        # noinspection PyTypeChecker
        return LogLevel[self.value]


class LogMessage(BaseModel):
    timestamp: datetime = Field(description="Timestamp of the log message")
    id_app: str = Field(description="Reference to the application")
    level: LogLevelName = Field(description="Log level")
    message: str = Field(description="Message text")
    metadata: Optional["MessageMetadata"] = Field(description="Additional information from LogRecord", default=None)

    @field_validator("timestamp")
    @classmethod
    def validate_ts(cls, value: datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=SYSTEM_TZ)
        return value

    @field_serializer("timestamp")
    def serialize_timestamps(self, ts: datetime):
        return ts.isoformat(timespec="milliseconds")

    @classmethod
    def from_log_record(cls, id_app: str, record: LogRecord, message_text: str):
        return LogMessage(
            timestamp=datetime.fromtimestamp(record.created),
            id_app=id_app,
            level=LogLevelName(record.levelname),
            message=message_text,
            metadata=MessageMetadata(
                exc_text=record.exc_text,
                filename=record.filename,
                line=record.lineno,
                func_name=record.funcName,
                name=record.name,
                process=record.process,
                process_name=record.processName,
                thread=record.thread,
                thread_name=record.threadName
            )
        )


class MessageMetadata(BaseModel):
    exc_text: Optional[str] | None
    filename: str
    line: int
    func_name: str
    name: str
    process: Optional[int]
    process_name: Optional[str]
    thread: Optional[int]
    thread_name: Optional[str]
