import abc

from pydantic import BaseModel, Field

from logmaster.server.core.models.resource import AppResource, MessageResource


class Page(BaseModel, abc.ABC):
    page_number: int = Field(description="Page number", ge=0)
    page_size: int = Field(description="Page size", ge=1)
    total_items: int = Field(description="Total number of items", ge=0)
    total_pages: int = Field(description="Total number of pages", ge=0)

    @property
    @abc.abstractmethod
    def content(self) -> list[BaseModel]:
        """The content of the page."""


class AppPage(Page):
    content: list[AppResource] = Field(description="Apps in the page")


class MessagePage(Page):
    content: list[MessageResource] = Field(description="Apps in the page")
