from datetime import datetime
from functools import singledispatchmethod
from typing import Any
from dataclasses import replace

from SincedPy.commands.command import CommandPattern
from SincedPy.commands.commands_util import print_and_pick
from SincedPy.database_handler import DatabaseHandler
from SincedPy.record import Record, RecordCategory, RecordStatus


class ModifyRecord(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        super().__init__(db_handler, *params)
        self._old_record: Record | None = None
        self._new_record: Record | None = None

    def execute(self) -> None:
        match self._params:
            case [title, option_param, *_]:
                option = DatabaseHandler.option_of_param(option_param)
                records = self._db_handler.filter_by(title)
            case _:
                err_msg = "Syndax for mod command: `mod <title> <new option>`"
                raise ValueError(err_msg)

        match records:
            case []:
                print("No records found")
            case [record]:
                self._save_replace(record, option)
            case _:
                record = print_and_pick(records)
                self._save_replace(record, option)

    def undo(self) -> None:
        if self._old_record is None or self._new_record is None:
            raise ValueError(
                f"No task was modified, cannot `undo` "
                f"({self._old_record=}, {self._new_record=})"
            )

        self._db_handler.replace_record(self._new_record, self._old_record)

    def _save_replace(self, old: Record, option: Any) -> None:
        self._old_record = old
        self._new_record = self._modify_old(option, self._old_record)
        self._db_handler.replace_record(old, self._new_record)

    @singledispatchmethod
    def _modify_old(self, option: Any, record: Record) -> Record:
        _ = record, option
        raise ValueError(f"Unsupported modification: {type(option)}")

    @_modify_old.register
    def _(self, option: RecordStatus, record: Record) -> Record:
        return replace(record, status=option)

    @_modify_old.register
    def _(self, option: RecordCategory, record: Record) -> Record:
        return replace(record, category=option.value)

    @_modify_old.register
    def _(self, option: str, record: Record) -> Record:
        return replace(record, title=option)

    @_modify_old.register
    def _(self, option: datetime, record: Record) -> Record:
        return replace(record, user_date=option)
