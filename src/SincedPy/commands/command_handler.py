from __future__ import annotations
import pickle

from pathlib import Path
import sys
from typing import Callable

from SincedPy.commands.command import CommandPattern
from SincedPy.common import get_ctx
from SincedPy.database_handler import DatabaseHandler

from .append_record import AppendRecord
from .log_records import LogRecords
from .modify_record import ModifyRecord
from .remove_records import RemoveRecords

type CommandFn = Callable[[tuple[str, ...], CommandPattern]]


class CommandHandler:
    def __init__(self, db_handler: DatabaseHandler) -> None:
        self.history = _CommandHistoryManager(get_ctx().HISORY_PATH, db_handler)
        self._commands: dict[str, CommandFn] = {
            "undo": lambda *_: _Undo(self.history),
            "add": lambda *args: AppendRecord(db_handler, *args),
            "log": lambda *args: LogRecords(db_handler, sys.stdout.write, *args),
            "mod": lambda *args: ModifyRecord(db_handler, *args),
            "rem": lambda *args: RemoveRecords(db_handler, *args),
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
        try:
            [command_name, *rest] = params
        except ValueError:
            print(f"Available commands: {_format_commands(self._commands)}")
            return

        if command_name == "help":
            self._handle_help(*rest)
            return

        command_builer = self._commands.get(command_name, None)
        if command_builer is None:
            print(f"There is no command named `{command_name}`")
            print(f"Available commands: {_format_commands(self._commands)}")
            return

        command = command_builer(*rest)
        command.execute()
        self.history.push(command)

    def _handle_help(self, *params) -> None:
        if len(params) == 0:
            print(_format_commands(self._commands))
            return

        cmd_builder = self._commands.get(params[0], None)
        if cmd_builder is None:
            print(f"There is no command named `{params[0]}`")
            print(f"Available commands: {_format_commands(self._commands)}")
            return

        print(cmd_builder(*params[1:]).help)


def _format_commands(commands: dict[str, Callable]) -> str:
    def fmt_cmd(cmd: str) -> str:
        return f"\n\t- {cmd}"

    return "".join(fmt_cmd(cmd) for cmd in commands.keys())


class _CommandHistoryManager:
    def __init__(self, history_path: Path, db_handler: DatabaseHandler) -> None:
        self._history_path = history_path
        self._db_handler = db_handler

    def push(self, cmd: CommandPattern) -> None:
        if not cmd.undoable:
            return
        with open(self._history_path, "ab") as history:
            pickle.dump(cmd, history)

    def pop(self) -> CommandPattern:
        cmds: list[CommandPattern] = []
        with open(self._history_path, "rb") as history:
            try:
                while True:
                    cmds.append(pickle.load(history))
            except EOFError:
                pass
        last = cmds.pop()
        with open(self._history_path, "wb") as history:
            for cmd in cmds:
                pickle.dump(cmd, history)
        last.db_handler = self._db_handler
        return last


class _Undo(CommandPattern):
    def __init__(self, history: _CommandHistoryManager) -> None:
        self._history = history
        self.undoable = False

    def execute(self):
        cmd = self._history.pop()
        cmd.undo()

    def undo(self) -> None:
        raise ValueError("Cannot undo the Undo")

    @property
    def help(self) -> str:
        return "Undo last command if possible (stackable)"
