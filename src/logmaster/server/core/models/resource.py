import abc
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from logmaster.core.logging import LogLevelName, MessageMetadata
from logmaster.server.core.models.document import AuditMetadata, App, Message


class Resource(BaseModel, abc.ABC):

    @classmethod
    def from_model(cls, model: Any):
        raise NotImplementedError("From model must be overwritten")


class AppResource(Resource):
    id: str = Field(description="Application identifier")
    name: str = Field(description="Application name")
    description: Optional[str] = Field(description="Application description", default=None)
    audit_meta: AuditMetadata = Field(description="Audit info")

    @classmethod
    def from_model(cls, app: App):
        return cls(**app.model_dump())


class MessageResource(Resource):
    timestamp: datetime = Field(description="Timestamp of the log message")
    id_app: str = Field(description="Reference to the application")
    level: LogLevelName = Field(description="Log level")
    message: str = Field(description="Message text")
    metadata: Optional[MessageMetadata] = Field(description="Additional information taken from LogRecord", default=None)

    @classmethod
    def from_model(cls, msg: Message):
        return cls(**msg.model_dump())
