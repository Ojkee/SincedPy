from functools import singledispatchmethod
from tinydb import TinyDB, Query
from datetime import datetime
from dateutil.relativedelta import relativedelta

from SincedPy.record import Record, RecordStatus, RecordCategory


class DatabaseHandler:
    def __init__(self, database: TinyDB) -> None:
        self._db = database

    def make_record(self, *record_data: str, category: str | None = None) -> Record:
        match record_data:
            case (title,):
                return Record(title, category=category)
            case (title, user_date):
                user_date = datetime.fromisoformat(user_date)
                return Record(title, user_date=user_date)
            case (title, user_date, flag, flag_param) if flag.startswith("-"):
                try:
                    n = int(flag_param)
                except ValueError:
                    err_msg = f"Value after {flag} needs to be a number"
                    raise ValueError(err_msg) from None
                delta = self.make_delta(flag[1:], n)
                user_date = datetime.fromisoformat(user_date)
                return Record(title, user_date=user_date, recurring_delta=delta)
            case _:
                raise ValueError("INVALID INPUT - TODO: make helper msg")

    def append_record(self, record: Record) -> None:
        self._db.insert(record.to_dict())

    def log_all(self) -> None:
        records = list(map(Record.from_dict, self._db.all()))
        if len(records) == 0:
            print("No records")
            return
        for record in records:
            print(record)

    @singledispatchmethod
    def log_by(self, obj: object) -> None:
        not_impl_err = f"Log dispatch not implemented for type `{type(obj).__name__}`"
        raise NotImplementedError(not_impl_err)

    @log_by.register
    def _(self, status: RecordStatus) -> None:
        record_q = Query()
        record = self._db.get(record_q.status == status.value)
        assert not isinstance(record, list)
        if record is None:
            print(f"no record titled `{status}`")
            return
        print(Record.from_dict(record))

    @log_by.register
    def _(self, title: str) -> None:
        record_q = Query()
        record = self._db.get(record_q.title == title)
        assert not isinstance(record, list)
        if record is None:
            print(f"no record titled `{title}`")
            return
        print(Record.from_dict(record))

    @log_by.register
    def _(self, category: RecordCategory) -> None:
        category_q = Query()
        records = self._db.search(category_q.category == category.value)
        if records is None:
            print(f"no category `{category.value}`")
            return

        if not isinstance(records, list) and records is not None:
            print(Record.from_dict(records))

        for record in map(Record.from_dict, records):
            print(record)

    def drop_all(self) -> None:
        self._db.drop_tables()

    def make_delta(self, flag: str, n: int) -> relativedelta:
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
