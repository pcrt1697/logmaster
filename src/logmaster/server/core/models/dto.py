import abc
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from logmaster.core.logging import LogLevelName, MessageMetadata, LogMessage
from logmaster.server.core.models.document import App, AuditMetadata
from logmaster.server.core.models.search import Filter, Sort, AppSort, MessageSort, MessageFilter


class AppInput(BaseModel):
    name: str = Field(description="Application name")
    description: Optional[str] = Field(description="Application description", default=None)

    def to_document(self, _id: str):
        return App(
            id=_id,
            name=self.name,
            description=self.description,
            audit_meta=AuditMetadata.create()
        )


class PageInput(BaseModel, abc.ABC):
    page_number: int = Field(description="Page number", ge=0)
    page_size: int = Field(description="Page size", ge=1)

    def get_filter(self) -> Filter | None:
        return None

    @abc.abstractmethod
    def get_sort(self) -> Sort:
        pass

    def get_offset(self):
        return self.page_number * self.page_size


class AppPageInput(PageInput):
    sort: Optional[AppSort] = Field(description="Sorting definition. The default is ascending by id.", default=None)

    def get_sort(self) -> AppSort:
        return self.sort


class MessageInput(BaseModel):
    timestamp: datetime = Field(description="Timestamp of the log message")
    id_app: str = Field(description="Reference to the application")
    level: LogLevelName = Field(description="Log level")
    message: str = Field(description="Message text")
    metadata: Optional[MessageMetadata] = Field(description="Additional information taken from LogRecord", default=None)

    def to_log_message(self) -> LogMessage:
        return LogMessage(
            timestamp=self.timestamp,
            id_app=self.id_app,
            level=self.level,
            message=self.message,
            metadata=self.metadata
        )


class MessagePageInput(PageInput):
    sort: Optional[MessageSort] = Field(description="Sorting definition. The default is descending by timestamp.", default=None)
    filter: Optional[MessageFilter] = Field(description="Filter query.", default=None)

    def get_filter(self) -> MessageFilter | None:
        return self.filter

    def get_sort(self) -> MessageSort:
        return self.sort
