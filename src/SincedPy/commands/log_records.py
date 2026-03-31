from SincedPy.commands.command import CommandPattern
from SincedPy.database_handler import DatabaseHandler


class LogRecords(CommandPattern):
    def __init__(self, db_handler: DatabaseHandler, out_stream, *params: str) -> None:
        super().__init__(db_handler, *params)
        self.undoable = False
        self.out_stream = out_stream

    def execute(self) -> None:
        if len(self._params) == 0:
            records = self._db_handler.all_records()
        else:
            option = DatabaseHandler.option_of_param(self._params[0])
            records = self._db_handler.filter_by(option)

        records = map(lambda r: r.next_appearance(), records)
        records = sorted(records, key=lambda r: (r.user_date is None, r.user_date))
        records = [str(record) for record in records]
        records_str = "\n".join(records) if len(records) > 0 else "No records"
        self.out_stream(records_str + "\n")

    def undo(self) -> None:
        print("Cannot `undo` logging")

    @property
    def help(self) -> str:
        return """
log            # logs all
log name       # logs records with name
log -[d/w/m/y] # logs records in day/week/month/year
log @category  # logs records from category
log status     # logs records with status
"""
