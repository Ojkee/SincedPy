import sys
from typing import Callable

from SincedPy.commands import AppendRecord, LogRecords, RemoveRecords, ModifyRecord
from SincedPy.common import get_db_handler


def main(params: list[str]) -> None:
    handler = get_db_handler()

    commands: dict[str, Callable] = {
        "add": lambda *args: AppendRecord(handler, *args),
        "log": lambda *args: LogRecords(handler, *args),
        "mod": lambda *args: ModifyRecord(handler, *args),
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
    try:
        command.execute()
    except NotImplementedError as e:
        print(f"Not yet implemented:\n\t{e}")


def format_commands(commands: dict[str, Callable]) -> str:
    def fmt_cmd(cmd: str) -> str:
        return f"\n\t- {cmd}"

    return "".join(map(fmt_cmd, commands.keys()))


if __name__ == "__main__":
    main(sys.argv[1:])
