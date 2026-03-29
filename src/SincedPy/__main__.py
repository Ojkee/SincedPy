import sys

from SincedPy.database_handler import get_db_handler
from SincedPy.commands import CommandHandler


def main() -> None:
    params = sys.argv[1:]
    db_handler = get_db_handler()

    with CommandHandler(db_handler) as cmd_handler:
        cmd_handler.run(*params)


if __name__ == "__main__":
    main()
