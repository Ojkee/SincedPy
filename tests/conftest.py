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
def freeze_records():
    def freeze_one(r: Record) -> Record:
        r.date_created = datetime(2000, 1, 1)
        return r

    def freezer(records: list[Record]) -> list[Record]:
        return list(map(freeze_one, records))

    return freezer
