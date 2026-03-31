from abc import ABC, abstractmethod

from SincedPy.database_handler import DatabaseHandler


class CommandPattern(ABC):
    def __init__(self, db_handler: DatabaseHandler, *params: str) -> None:
        self.undoable = True
        self._db_handler = db_handler
        self._params = list(params)

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

    @property
    @abstractmethod
    def help(self) -> str: ...

    @property
    def db_handler(self) -> DatabaseHandler:
        if self._db_handler is None:
            raise ValueError(f"Need to set database handler for {type(self).__name__}")
        return self._db_handler

    @db_handler.setter
    def db_handler(self, value: DatabaseHandler) -> None:
        self._db_handler = value

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        state["_db_handler"] = None
        return state

    def __setstate__(self, state) -> None:
        self.__dict__.update(state)  # type: ignore
