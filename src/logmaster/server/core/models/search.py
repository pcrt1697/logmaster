import abc
from datetime import datetime, date
from enum import StrEnum
from typing import Union, Mapping, Any, Literal, Optional, Annotated

from beanie.odm.operators.find.comparison import In, NotIn, NE, Eq, LT, GTE, GT, LTE
from beanie.odm.operators.find.evaluation import RegEx, Text
from pydantic import BaseModel, Field

from logmaster.server.core.models.document import Message


class SortDirection(StrEnum):
    ASC = "ASC"
    DESC = "DESC"

    def get_sign(self):
        if self == SortDirection.ASC:
            return "+"
        return "-"


class FilterOperator(BaseModel, abc.ABC):

    @property
    @abc.abstractmethod
    def operator(self) -> str:
        """The operator name."""

    @abc.abstractmethod
    def to_criteria(self, field_reference):
        pass


class EqOperator(FilterOperator):
    operator: Literal["eq"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return Eq(field_reference, self.value)


class NeOperator(FilterOperator):
    operator: Literal["ne"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return NE(field_reference, self.value)


class InOperator(FilterOperator):
    operator: Literal["in"] = Field(description="Filter operator")
    values: list[Union[str|int|float|bool|datetime|date]]

    def to_criteria(self, field_reference):
        return In(field_reference, self.value)


class NinOperator(FilterOperator):
    operator: Literal["nin"] = Field(description="Filter operator")
    values: list[Union[str | int | float | bool | datetime | date]]

    def to_criteria(self, field_reference):
        return NotIn(field_reference, self.value)


class LtOperator(FilterOperator):
    operator: Literal["lt"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return LT(field_reference, self.value)


class LteOperator(FilterOperator):
    operator: Literal["lte"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return LTE(field_reference, self.value)


class GtOperator(FilterOperator):
    operator: Literal["gt"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return GT(field_reference, self.value)


class GteOperator(FilterOperator):
    operator: Literal["gte"] = Field(description="Filter operator")
    value: Union[str|int|float|bool|datetime|date]

    def to_criteria(self, field_reference):
        return GTE(field_reference, self.value)


class IsNullOperator(FilterOperator):
    operator: Literal["nu"] = Field(description="Filter operator")

    def to_criteria(self, field_reference):
        return Eq(field_reference, None)


class NotNullOperator(FilterOperator):
    operator: Literal["nn"] = Field(description="Filter operator")

    def to_criteria(self, field_reference):
        return NE(field_reference, None)


class RegexOperator(FilterOperator):
    operator: Literal["regex"] = Field(description="Filter operator")
    pattern: str
    option: Optional[str]

    def to_criteria(self, field_reference):
        return RegEx(field_reference, self.pattern, self.options)


class SearchOperator(FilterOperator):
    operator: Literal["search"] = Field(description="Filter operator")
    value: str

    def to_criteria(self, field_reference):
        return Text(self.value)


class Sort(BaseModel, abc.ABC):

    def get_sort(self) -> list[str]:
        return self._get_sort() or ["+id"]

    @abc.abstractmethod
    def _get_sort(self) -> list[str]:
        pass


class Filter(BaseModel, abc.ABC):

    @abc.abstractmethod
    def get_criteria(self) -> Union[Mapping[str, Any], bool] | None:
        pass


class AppSort(Sort):
    name: SortDirection = Field(description="Sort by name")

    def _get_sort(self) -> list[str]:
        return [self.name.get_sign() + "name"]


class MessageSort(Sort):
    timestamp: SortDirection = Field(description="Sort by timestamp")

    def _get_sort(self) -> list[str]:
        return [self.timestamp.get_sign() + "timestamp"]


TimestampAndFilters = Annotated[
    Union[LtOperator|LteOperator|GtOperator|GteOperator],
    Field(discriminator="operator")
]


class MessageFilter(Filter):
    message: Optional[SearchOperator] = Field(description="Text to search inside the message", default=None)
    timestamp: Optional[TimestampAndFilters] = Field(
        description="Filter the timestamp",
        default=None
    )
    id_app: Optional[Union[RegexOperator|EqOperator|NeOperator|InOperator|NinOperator]] = Field(
        description="Filter the app",
        discriminator="operator",
        default=None
    )
    level: Optional[Union[RegexOperator|EqOperator|NeOperator|InOperator|NinOperator]] = Field(
        description="Filter the log level",
        discriminator="operator",
        default=None
    )

    def get_criteria(self) -> Union[Mapping[str, Any], bool] | None:
        criteria = ()
        if self.message:
            criteria += (self.message.to_criteria(Message.message), )
        if self.timestamp:
            criteria += (f.to_criteria(Message.timestamp) for f in self.timestamp)
        if self.id_app:
            criteria += (self.id_app.to_criteria(Message.id_app), )
        if self.level:
            criteria += (self.level.to_criteria(Message.level), )
        return criteria

