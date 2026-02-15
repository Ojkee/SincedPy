from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler, make_record
from SincedPy.record import Record, RecordCategory

from .commands_util import extract_one


class AppendRecord(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._record_params = list(params)
        self._new_record: Record | None = None

    def execute(self) -> None:
        category, self._record_params = extract_one(
            self._record_params, RecordCategory.valid
        )
        new_record = make_record(*self._record_params)
        new_record.category = category
        self._db_handler.append_record(new_record)

    def undo(self) -> None:
        if self._new_record is None:
            err_msg = "No task was added, cannot `undo` the AppendRecord command"
            raise RuntimeError(err_msg)

        self._db_handler.drop(self._new_record)
