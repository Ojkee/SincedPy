from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Protocol
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SupportStr(Protocol):
    def __str__(self) -> str: ...


class RecordStatus(Enum):
    ONGOING = "ONGOING"
    DONE = "DONE"
    CANCELED = "CANCELED"

    @classmethod
    def valid(cls, status: str) -> bool:
        return any(status.upper() == member.value for member in cls)

    @classmethod
    def from_str(cls, status: str) -> RecordStatus:
        status = status.upper()
        for member in cls:
            if status == member.value or status == member.name:
                return member
        raise ValueError(f"{status!r} in not a valid RecordStatus")


class RecordCategory:
    PREFIX = "@"

    def __init__(self, category: str) -> None:
        self._value = category

    @property
    def value(self) -> str:
        return RecordCategory._trim(self._value)

    @classmethod
    def _trim(cls, data: str) -> str:
        return data.lstrip(cls.PREFIX)

    @classmethod
    def valid(cls, category: str) -> bool:
        return category.startswith(cls.PREFIX)


@dataclass
class Record:
    title: str
    date_created: datetime = field(default_factory=datetime.now)
    category: str | None = field(default=None)
    user_date: datetime | None = field(default=None)
    recurring_delta: relativedelta | None = field(default=None)
    status: str = field(default=RecordStatus.ONGOING.value)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Record:
        parsed = {}
        for key, value in data.items():
            try:
                parsed[key] = datetime.fromisoformat(value)
            except (TypeError, ValueError):
                parsed[key] = value
        return cls(**parsed)

    def to_dict(self) -> dict[str, SupportStr]:
        return {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in self.__dict__.items()
        }

    def __str__(self) -> str:
        date = (
            self.user_date.strftime(" - %d/%m/%y") if self.user_date is not None else ""
        )
        return f"{self.title}{date}"
