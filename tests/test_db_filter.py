from dataclasses import dataclass
import pytest

from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record, RecordStatus


@dataclass
class Case:
    name: str
    all_records: list[Record]
    param: str
    expected: list[Record]


CASES: list[Case] = [
    Case(
        name="By Name",
        all_records=[
            Record("A"),
            Record("B"),
            Record("C"),
            Record("D"),
        ],
        param="C",
        expected=[Record("C")],
    ),
    Case(
        name="By Category",
        all_records=[
            Record("A", category="foo"),
            Record("B"),
            Record("C", category="bar"),
            Record("D", category="foo"),
        ],
        param="@foo",
        expected=[Record("A", category="foo"), Record("D", category="foo")],
    ),
    Case(
        name="By Status",
        all_records=[
            Record("A", category="foo"),
            Record("B", status=RecordStatus.DONE),
            Record("C", category="bar", status=RecordStatus.DONE),
            Record("D", category="foo", status=RecordStatus.CANCELED),
        ],
        param="done",
        expected=[
            Record("B", status=RecordStatus.DONE),
            Record("C", category="bar", status=RecordStatus.DONE),
        ],
    ),
]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.name)
def test_db_filtering(case: Case, db_handler: DatabaseHandler, freeze_records):
    all_records = freeze_records(case.all_records)
    expected = freeze_records(case.expected)

    for record in all_records:
        db_handler.append_record(record)

    option = DatabaseHandler.option_of_param(case.param)
    result = db_handler.filter_by(option)
    assert result == expected
