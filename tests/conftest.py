from datetime import datetime
from typing import Generator
import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record


@pytest.fixture
def db_handler() -> Generator[DatabaseHandler]:
    db = TinyDB(storage=MemoryStorage)
    yield DatabaseHandler(db)
    db.close()


@pytest.fixture
def precision_to_day():
    def set_one(r: Record) -> Record:
        new_date = datetime(
            r.date_created.year,
            r.date_created.month,
            r.date_created.day,
        )
        r.date_created = new_date
        if r.user_date is not None:
            new_user_date = datetime(
                r.user_date.year,
                r.user_date.month,
                r.user_date.day,
            )
            r.user_date = new_user_date
        return r

    def setter(records: list[Record]) -> list[Record]:
        return list(map(set_one, records))

    return setter
