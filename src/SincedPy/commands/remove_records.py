from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record, RecordCategory, RecordStatus


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
            case [category] if RecordCategory.valid(category):
                self._db_handler.drop_by(RecordCategory(category))
            case [status] if RecordStatus.valid(status):
                self._db_handler.drop_by(RecordStatus.from_str(status))
            case [name]:
                self._db_handler.drop_by(name)

    def undo(self) -> None:
        if self._record is None:
            err_msg = "No task was removed, cannot `undo`"
            raise RuntimeError(err_msg)
        self._db_handler.append_record(self._record)
