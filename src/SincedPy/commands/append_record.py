from functools import cache
from SincedPy.commands.command import CommandPattern
from SincedPy.common import get_ctx
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record, RecordCategory

from .commands_util import extract_one


class AppendRecord(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        super().__init__(db_handler, *params)
        self._new_record: Record | None = None

    def execute(self) -> None:
        category, self._params = extract_one(self._params, RecordCategory.valid)
        new_record = Record.of_params(*self._params)
        new_record.category = RecordCategory(category).value

        x = "y"
        similar_record = self._record_with_similar_title(new_record.title)
        if similar_record is not None:
            x = input(
                f"Found record with similar title: `{similar_record.title}`\n\tAdd anyway? [y/N]? "
            )
        if x == "y":
            self._db_handler.append_record(new_record)
        self._new_record = new_record

    def undo(self) -> None:
        if self._new_record is None:
            err_msg = "No task was added, cannot `undo`"
            raise RuntimeError(err_msg)

        self._db_handler.drop_by(self._new_record)

    @property
    def help(self) -> str:
        return """
add name                              # adds record 
add name @category                    # adds record that belongs to category
add name DD/MM/YYYY                   # adds record with deadline
add name DD/MM/YYYY -[d/w/m/y] number # adds recurring record, number is optional, eg. -w 8 => every 8 weeks, You can use @category
"""

    def _record_with_similar_title(self, title: str) -> Record | None:
        ctx = get_ctx()
        for record in self._db_handler.all_records():
            if record.title == title:
                return record
            if (
                len(record.title) > ctx.SPELLING_DISTANCE
                and levenshtein(record.title, title) <= ctx.SPELLING_DISTANCE
            ):
                return record

        return None


@cache
def levenshtein(a: str, b: str) -> int:
    if len(b) == 0:
        return len(a)
    if len(a) == 0:
        return len(b)
    if a[0] == b[0]:
        return levenshtein(a[1:], b[1:])

    return 1 + min(
        levenshtein(a[1:], b),
        levenshtein(a, b[1:]),
        levenshtein(a[1:], b[1:]),
    )
