from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record


class RemoveRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)
        self._record: Record | None = None

    def execute(self) -> None:
        match self._params:
            case []:
                raise ValueError("Need to provide more context")
            case ["all"]:
                x = input("You sure (y/n)? ")
                if x.lower() in ["y", "yes"]:
                    self._db_handler.drop_all()
            case [param, *_]:
                option = DatabaseHandler.option_of_param(param)
                self._db_handler.drop_by(option)

    def undo(self) -> None:
        if self._record is None:
            err_msg = "No task was removed, cannot `undo`"
            raise RuntimeError(err_msg)
        self._db_handler.append_record(self._record)
