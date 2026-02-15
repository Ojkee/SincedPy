from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import RecordCategory, RecordStatus


class LogRecords(CommandPattern):
    _validators = [
        (RecordCategory.valid, lambda c: RecordCategory(c)),
        (RecordStatus.valid, lambda s: RecordStatus.from_str(s)),
    ]

    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)

    def execute(self) -> None:
        if len(self._params) == 0:
            self._db_handler.log_all()
            return

        param = self._params[0]
        option = param
        for valid, factory in self._validators:
            if valid(param):
                option = factory(param)
                break

        self._db_handler.log_by(option)

    def undo(self) -> None:
        print("Cannot `undo` logging")
