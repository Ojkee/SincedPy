from tinydb import TinyDB, Query
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

from SincedPy.record import Record


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
                    raise ValueError(
                        f"value after {flag} needs to be a number"
                    ) from None
                delta = self.make_delta(flag[1:], n)
                user_date = datetime.fromisoformat(user_date)
                return Record(title, user_date=user_date, recurring_delta=delta)
            case _:
                raise ValueError("INVALID INPUT - TODO: make helper msg")

    def append_record(self, record: Record) -> None:
        self._db.insert(record.to_dict())

    def log_all(self) -> None:
        records = self._db.all()
        pprint(records or "No records")

    def log_record(self, title: str) -> None:
        record_q = Query()
        record = self._db.get(record_q.title == title)
        assert not isinstance(record, list)
        if record is None:
            print(f"no record titled `{title}`")
            return
        print(Record.from_dict(record))

    def log_category(self, category: str) -> None:
        category_q = Query()
        records = self._db.search(category_q.category == category)
        if records is None:
            print(f"no category `{category}`")
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
