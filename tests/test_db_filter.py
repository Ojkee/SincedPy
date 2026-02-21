from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
    Case(
        name="By Delta: Week",
        all_records=[
            Record("A", user_date=datetime.now() + relativedelta(days=1)),
            Record("B"),
            Record("C"),
            Record("D"),
        ],
        param="-w",
        expected=[
            Record("A", user_date=datetime.now() + relativedelta(days=1)),
        ],
    ),
    Case(
        name="By Delta: Year with recurring",
        all_records=[
            Record("A", user_date=datetime.now() - relativedelta(years=3, months=2)),
            Record(
                "B",
                user_date=datetime.now() - relativedelta(years=3, months=2),
                recurring_delta=relativedelta(years=1),
            ),
            Record("C"),
            Record("D", user_date=datetime.now() + relativedelta(months=2)),
            Record("E", user_date=datetime.now() + relativedelta(years=1, months=1)),
            Record(
                "F",
                user_date=datetime.now() - relativedelta(years=1, months=11),
                recurring_delta=relativedelta(months=1),
            ),
        ],
        param="-y",
        expected=[
            Record(
                "B",
                user_date=datetime.now()
                - relativedelta(years=3, months=2)
                + relativedelta(years=4),
                recurring_delta=relativedelta(years=1),
            ),
            Record("D", user_date=datetime.now() + relativedelta(months=2)),
            Record(
                "F",
                user_date=datetime.now()
                - relativedelta(years=1, months=11)
                + relativedelta(years=2),
                recurring_delta=relativedelta(months=1),
            ),
        ],
    ),
]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.name)
def test_db_filtering(case: Case, db_handler: DatabaseHandler, precision_to_day):
    all_records = precision_to_day(case.all_records)
    expected = precision_to_day(case.expected)

    for record in all_records:
        db_handler.append_record(record)

    option = DatabaseHandler.option_of_param(case.param)
    result = db_handler.filter_by(option)
    assert result == expected
