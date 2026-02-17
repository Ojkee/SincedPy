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

    def __str__(self) -> str:
        return self.value


class RecordCategory:
    PREFIX = "@"

    def __init__(self, category: str | None) -> None:
        self._value = category

    @property
    def value(self) -> str | None:
        return RecordCategory._trim(self._value) if self._value is not None else None

    @classmethod
    def _trim(cls, data: str) -> str:
        return data.lstrip(cls.PREFIX)

    @classmethod
    def valid(cls, category: str) -> bool:
        return category.startswith(cls.PREFIX)

    def __str__(self) -> str:
        if self.value is None:
            return "None"
        return self.value


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
            if value == "None":
                parsed[key] = None
        return cls(**parsed)

    def to_dict(self) -> dict[str, SupportStr]:
        parsed: dict[str, SupportStr] = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                parsed[key] = value.isoformat()
            else:
                parsed[key] = str(value)
        return parsed

    def __str__(self) -> str:
        date = (
            self.user_date.strftime(" - %d/%m/%y") if self.user_date is not None else ""
        )
        return f"{self.title}{date}"

    @classmethod
    def of_params(cls, *record_data: str) -> Record:
        match record_data:
            case (title,):
                return Record(title)
            case (title, user_date):
                user_date = datetime.fromisoformat(user_date)
                return Record(title, user_date=user_date)
            case (title, user_date, flag, flag_param) if flag.startswith("-"):
                try:
                    n = int(flag_param)
                except ValueError:
                    err_msg = f"Value after {flag} needs to be a number"
                    raise ValueError(err_msg) from None
                delta = make_delta(flag[1:], n)
                user_date = datetime.fromisoformat(user_date)
                return Record(title, user_date=user_date, recurring_delta=delta)
            case _:
                raise ValueError("INVALID INPUT - TODO: make helper msg")


def make_delta(flag: str, n: int) -> relativedelta:
    match flag:
        case "y":
            return relativedelta(years=n)
        case "m":
            return relativedelta(months=n)
        case "w":
            return relativedelta(weeks=n)
        case "d":
            return relativedelta(days=n)
        case _:
            raise ValueError(f"Invalid flag: {flag}, pick from y/m/w/d")
