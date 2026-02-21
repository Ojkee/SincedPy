from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler


class LogRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)

    def execute(self) -> None:
        if len(self._params) == 0:
            records = list(self._db_handler.all_records())
            print("No record fulfills this cirteria" if len(records) == 0 else records)
            return

        option = DatabaseHandler.option_of_param(self._params[0])
        records = self._db_handler.filter_by(option)
        print("No record fullfil this cirteria" if len(records) == 0 else records)

    def undo(self) -> None:
        print("Cannot `undo` logging")
