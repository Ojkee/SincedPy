from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import RecordCategory, RecordStatus, make_delta


class LogRecords(CommandPattern):
    _validators = [
        (RecordCategory.valid, lambda c: RecordCategory(c)),
        (RecordStatus.valid, lambda s: RecordStatus.from_str(s)),
        (lambda f: f in ["-y", "-m", "-w", "-d"], lambda f: make_delta(f)),
    ]

    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)

    def execute(self) -> None:
        if len(self._params) == 0:
            records = list(self._db_handler.all_records())
            print("No record fulfills this cirteria" if len(records) == 0 else records)
            return

        param = self._params[0]
        option = param
        for valid, factory in self._validators:
            if valid(param):
                option = factory(param)
                break

        records = self._db_handler.filter_by(option)
        print("No record fullfil this cirteria" if len(records) == 0 else records)

    def undo(self) -> None:
        print("Cannot `undo` logging")
