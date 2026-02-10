import sys
from pathlib import Path

from tinydb import TinyDB

from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import RecordCategory, RecordStatus

_DATA_PATH = Path(__file__).parents[2] / "records" / "data.json"


def main(params: list[str]) -> None:
    db = TinyDB(_DATA_PATH)
    handler = DatabaseHandler(db)

    match params:
        case ["add", category, *record] if RecordCategory.valid(category):
            new_record = handler.make_record(*record)
            new_record.category = category[1:]
            handler.append_record(new_record)
        case ["add", *record]:
            new_record = handler.make_record(*record)
            handler.append_record(new_record)
        case ["log", category] if RecordCategory.valid(category):
            handler.log_by(RecordCategory(category))
        case ["log", status] if RecordStatus.valid(status):
            handler.log_by(RecordStatus.from_str(status))
        case ["log", record_name]:
            handler.log_by(record_name)
        case ["log"]:
            handler.log_all()
        case ["REMOVE!"]:
            handler.drop_all()
        case _:
            raise NotImplementedError("match/case in main")


if __name__ == "__main__":
    main(sys.argv[1:])
