from __future__ import annotations
from enum import IntEnum, auto
from dataclasses import dataclass, field
from typing import Any, Protocol
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SupportStr(Protocol):
    def __str__(self) -> str: ...


class RecordStatus(IntEnum):
    ONGOING = auto()
    DONE = auto()
    CANCELED = auto()


@dataclass
class Record:
    title: str
    date_created: datetime = field(default_factory=datetime.now)
    category: str | None = field(default=None)
    user_date: datetime | None = field(default=None)
    recurring_delta: relativedelta | None = field(default=None)
    status: RecordStatus = field(default=RecordStatus.ONGOING)

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
