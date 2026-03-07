from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record


class RemoveRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._records: list[Record] | None = None
        super().__init__(db_handler, *params)

    def execute(self) -> None:
        match self._params:
            case []:
                raise ValueError("Need to provide more context")
            case ["all"]:
                x = input("You sure [y/N]? ")
                if x.lower() in ["y", "yes"]:
                    self._records = list(self._db_handler.all_records())
                    self._db_handler.drop_all()
            case [param, *_]:
                option = DatabaseHandler.option_of_param(param)
                self._records = self._db_handler.filter_by(option)
                self._db_handler.drop_by(option)

    def undo(self) -> None:
        if self._records is None:
            err_msg = "No task was removed, cannot `undo`"
            raise RuntimeError(err_msg)
        for record in self._records:
            self._db_handler.append_record(record)
