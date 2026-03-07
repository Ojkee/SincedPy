from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler


class LogRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)
        self.undoable = False

    def execute(self) -> None:
        if len(self._params) == 0:
            records = self._db_handler.all_records()
        else:
            option = DatabaseHandler.option_of_param(self._params[0])
            records = self._db_handler.filter_by(option)

        records = map(lambda r: r.next_appearance(), records)
        records = sorted(records, key=lambda r: (r.user_date is None, r.user_date))
        records = list(map(repr, records))
        records_str = (
            "\n".join(records)
            if len(records) > 0
            else "No record fullfil this cirteria"
        )
        print(records_str)

    def undo(self) -> None:
        print("Cannot `undo` logging")
