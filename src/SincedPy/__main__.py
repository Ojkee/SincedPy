import sys
from pathlib import Path
from typing import Callable

from tinydb import TinyDB

from SincedPy.database_handler import DatabaseHandler
from SincedPy.commands import AppendRecord, LogRecords, RemoveRecords

_RECORDS_PATH = Path(__file__).parents[2] / "records" / "data.json"


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
        return

    command = command_builer(*rest)
    command.execute()


if __name__ == "__main__":
    main(sys.argv[1:])
