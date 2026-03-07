from __future__ import annotations
from typing import Callable

from SincedPy.database_handler import DatabaseHandler
from .append_record import AppendRecord
from .log_records import LogRecords
from .modify_record import ModifyRecord
from .remove_records import RemoveRecords


class CommandHandler:
    def __init__(self, db_handler: DatabaseHandler) -> None:
        self._commands: dict[str, Callable] = {
            "add": lambda *args: AppendRecord(db_handler, *args),
            "log": lambda *args: LogRecords(db_handler, *args),
            "mod": lambda *args: ModifyRecord(db_handler, *args),
            "rem": lambda *args: RemoveRecords(db_handler, *args),
            "remove": lambda *args: RemoveRecords(db_handler, *args),
            "REMOVE!": lambda *_: RemoveRecords(db_handler, "all"),
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        _ = exc_tb
        if exc_type is NotImplementedError:
            print(exc_val)
            return True
        return False

    def run(self, *params) -> None:
        match params:
            case ["undo", *_]:
                self._undo()
                return
        [command_name, *rest] = params
        command_builer = self._commands.get(command_name, None)
        if command_builer is None:
            print(f"There is no command named `{command_name}`")
            print(f"Available commands: {_format_commands(self._commands)}")
            return

        command = command_builer(*rest)
        command.execute()

    def _undo(self) -> None:
        pass


def _format_commands(commands: dict[str, Callable]) -> str:
    def fmt_cmd(cmd: str) -> str:
        return f"\n\t- {cmd}"

    return "".join(map(fmt_cmd, commands.keys()))
