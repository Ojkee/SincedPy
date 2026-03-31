from __future__ import annotations
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol
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


class RecordDate:
    _USER_FORMAT = "%d/%m/%Y"
    _SHORT_FORMAT = "%d/%m"
    _VALID_FORMATS = (
        _USER_FORMAT,
        _SHORT_FORMAT,
    )

    @classmethod
    def valid(cls, date: str) -> bool:
        try:
            for fmt in cls._VALID_FORMATS:
                datetime.strptime(date, fmt)
            return True
        except ValueError:
            return False

    @classmethod
    def parse(cls, date: str) -> datetime:
        try:
            return datetime.strptime(date, cls._USER_FORMAT)
        except ValueError:
            pass

        try:
            parsed = datetime.strptime(date, cls._SHORT_FORMAT)
            now = datetime.now()
            candidate = parsed.replace(year=now.year)
            if candidate.date() < now.date():
                candidate = candidate.replace(year=now.year + 1)
        except ValueError:
            raise ValueError(
                f"Invalid date format: {date!r}. Wanted dd/mm/yyyy"
            ) from None

        return candidate


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
        ctors: list[Callable[[str], Any]] = [
            datetime.fromisoformat,
            relativedelta_of_string,
            RecordStatus.from_str,
        ]
        parsed = {}
        for key, value in data.items():
            if value == "None":
                parsed[key] = None
                continue
            for ctor in ctors:
                field = field_of_string(value, ctor)
                if field is not None:
                    parsed[key] = field
                    break
                else:
                    parsed[key] = value

        return cls(**parsed)

    def to_dict(self) -> dict[str, SupportStr]:
        parsed: dict[str, SupportStr] = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                parsed[key] = value.isoformat()
            elif isinstance(value, relativedelta):
                parsed[key] = string_of_delta(value)
            else:
                parsed[key] = str(value)

        return parsed

    def __str__(self) -> str:
        category = f" @{self.category}" if self.category else ""
        date = (
            self.user_date.strftime(" - %d/%m/%Y") if self.user_date is not None else ""
        )
        return f"{self.title}{category}{date}"

    def __repr__(self) -> str:
        return str(self.to_dict())

    @classmethod
    def of_params(cls, *record_data: str) -> Record:
        match record_data:
            case (title,):
                return Record(title)
            case (title, user_date):
                user_date = RecordDate.parse(user_date)
                return Record(title, user_date=user_date)
            case (title, user_date, flag) if flag.startswith("-"):
                delta = make_delta(flag[1:])
                user_date = RecordDate.parse(user_date)
                return Record(title, user_date=user_date, recurring_delta=delta)
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

    def next_appearance(self) -> Record:
        if not self.recurring_delta or not self.user_date:
            return self

        new_date = self.user_date
        now = datetime.now()

        while new_date < now:
            new_date += self.recurring_delta

        return Record(
            title=self.title,
            date_created=self.date_created,
            category=self.category,
            user_date=new_date,
            recurring_delta=self.recurring_delta,
            status=self.status,
        )


def make_delta(flag: str, n: int = 1) -> relativedelta:
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


def field_of_string[T](field: str, ctor: Callable[[str], T]) -> T | None:
    try:
        return ctor(field)
    except (TypeError, ValueError):
        return None


def rd_to_dict(rd: relativedelta) -> dict[str, int]:
    return {
        "years": rd.years,
        "months": rd.months,
        "weeks": rd.weeks,
        "days": rd.days,
    }


def relativedelta_of_string(field: str) -> relativedelta | None:
    try:
        return relativedelta(**json.loads(field))
    except json.JSONDecodeError:
        return None


def string_of_delta(delta: relativedelta) -> str:
    return json.dumps(rd_to_dict(delta))
