from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler


class RemoveRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self._db_handler = db_handler
        self._params = list(params)

    def execute(self) -> None:
        match self._params:
            case []:
                raise ValueError("Need to provide more context")
            case ["all"]:
                x = input("You sure? ")
                if x.lower() in ["y", "yes"]:
                    self._db_handler.drop_all()

    def undo(self) -> None:
        pass
