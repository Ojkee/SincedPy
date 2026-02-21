import sys
from pathlib import Path
from typing import Callable

from tinydb import TinyDB

from SincedPy.database_handler import DatabaseHandler
from SincedPy.commands import AppendRecord, LogRecords, RemoveRecords

_RECORD_DIR_PATH = Path(__file__).parents[2] / "records"
_RECORDS_PATH = _RECORD_DIR_PATH / "data.json"
# _HISORY_PATH = _RECORDS_DIR_PATH / "history.json"


def main(params: list[str]) -> None:
    records_db = TinyDB(_RECORDS_PATH)
    handler = DatabaseHandler(records_db)
    commands: dict[str, Callable] = {
        "add": lambda *args: AppendRecord(handler, *args),
        "log": lambda *args: LogRecords(handler, *args),
        "rem": lambda *args: RemoveRecords(handler, *args),
        "remove": lambda *args: RemoveRecords(handler, *args),
        "REMOVE!": lambda *_: RemoveRecords(handler, "all"),
    }

    [command_name, *rest] = params
    command_builer = commands.get(command_name, None)
    if command_builer is None:
        print(f"There is no command named `{command_name}`")
        print(f"Available commands: {format_commands(commands)}")
        return

    command = command_builer(*rest)
    command.execute()


def format_commands(commands: dict[str, Callable]) -> str:
    def fmt_cmd(cmd: str) -> str:
        return f"\n\t- {cmd}"

    return "".join(map(fmt_cmd, commands.keys()))


if __name__ == "__main__":
    main(sys.argv[1:])
