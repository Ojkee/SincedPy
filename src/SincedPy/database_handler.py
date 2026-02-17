from functools import singledispatchmethod
from tinydb import TinyDB, Query

from SincedPy.record import Record, RecordStatus, RecordCategory


class DatabaseHandler:
    def __init__(self, database: TinyDB) -> None:
        self._db = database

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
