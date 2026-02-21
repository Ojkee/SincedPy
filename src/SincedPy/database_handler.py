from datetime import datetime
from functools import singledispatchmethod
from typing import Any, Generator
from dateutil.relativedelta import relativedelta
from tinydb import TinyDB, Query

from SincedPy.record import Record, RecordStatus, RecordCategory, make_delta


class DatabaseHandler:
    def __init__(self, database: TinyDB) -> None:
        self._db = database

    def append_record(self, record: Record) -> None:
        self._db.insert(record.to_dict())

    def all_records(self) -> Generator[Record]:
        for rec in map(Record.from_dict, self._db.all()):
            yield rec

    @singledispatchmethod
    def filter_by(self, obj: object) -> list[Record]:
        not_impl_err = f"Log dispatch not implemented for type `{type(obj).__name__}`"
        raise NotImplementedError(not_impl_err)

    @filter_by.register
    def _(self, title: str) -> list[Record]:
        record_q = Query()
        record = self._db.get(record_q.title == title)
        assert not isinstance(record, list)
        if record is None:
            return []
        return [Record.from_dict(record)]

    @filter_by.register
    def _(self, status: RecordStatus) -> list[Record]:
        category_q = Query()
        records = self._db.search(category_q.status == status.value)
        if records is None:
            return []

        if not isinstance(records, list):
            return [Record.from_dict(records)]

        return list(map(Record.from_dict, records))

    @filter_by.register
    def _(self, category: RecordCategory) -> list[Record]:
        category_q = Query()
        records = self._db.search(category_q.category == category.value)
        if records is None:
            return []

        if not isinstance(records, list):
            return [Record.from_dict(records)]

        return list(map(Record.from_dict, records))

    @filter_by.register
    def _(self, delta: relativedelta) -> list[Record]:
        next_appears = map(lambda r: r.next_appearance(), self.all_records())
        lhs = datetime.now()
        rhs = lhs + delta

        def in_time_range(r: Record) -> bool:
            return r.user_date is not None and lhs <= r.user_date <= rhs

        return list(filter(in_time_range, next_appears))

    def drop_all(self) -> None:
        self._db.drop_tables()

    @singledispatchmethod
    def drop_by(self, obj: object) -> None:
        not_impl_err = (
            f"Remove dispatch not implemented for type `{type(obj).__name__}`"
        )
        raise NotImplementedError(not_impl_err)

    @drop_by.register
    def _(self, category: RecordCategory) -> None:
        category_q = Query()
        self._db.remove(category_q.category == category.value)

    @drop_by.register
    def _(self, status: RecordStatus) -> None:
        status_q = Query()
        self._db.remove(status_q.status == status.value)

    @drop_by.register
    def _(self, title: str) -> None:
        name_q = Query()
        self._db.remove(name_q.title == title)

    @staticmethod
    def option_of_param(param: str) -> Any:
        validators = [
            (RecordCategory.valid, lambda c: RecordCategory(c)),
            (RecordStatus.valid, lambda s: RecordStatus.from_str(s)),
            (lambda f: f in ["-y", "-m", "-w", "-d"], lambda f: make_delta(f)),
        ]

        for valid, factory in validators:
            if valid(param):
                return factory(param)
        return param
