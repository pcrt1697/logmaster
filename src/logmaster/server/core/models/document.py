from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field, BaseModel

from logmaster.core.logging import LogLevelName, MessageMetadata


class AuditMetadata(BaseModel):
    ts_insert: datetime
    ts_update: datetime

    def update(self):
        self.ts_update = datetime.now()

    @classmethod
    def create(cls):
        ts = datetime.now()
        return AuditMetadata(ts_insert=ts, ts_update=ts)


class App(Document):
    id: str = Field(description="Application identifier")
    name: str = Field(description="Application name")
    description: Optional[str] = Field(description="Application description", default=None)
    audit_meta: AuditMetadata = Field(description="Audit info")

    class Settings:
        name = "apps"
        keep_nulls = False


class Message(Document):
    timestamp: datetime = Field(description="Timestamp of the log message")
    id_app: str = Field(description="Reference to the application")
    level: LogLevelName = Field(description="Log level")
    message: str = Field(description="Message text")
    metadata: Optional[MessageMetadata] = Field(description="Additional information taken from LogRecord", default=None)

    class Settings:
        name = "messages"
        keep_nulls = False


DOCUMENT_MODELS = (App, Message)
