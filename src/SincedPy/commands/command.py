from abc import ABC, abstractmethod


class CommandPattern(ABC):
    def __init__(self) -> None:
        self.undoable = True

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass
