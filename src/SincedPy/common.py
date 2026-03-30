import os
from platformdirs import user_data_dir
from pathlib import Path


class Context:
    SPELLING_DISTANCE = 2

    if os.environ.get("SCD_DEV"):
        RECORD_DIR_PATH = Path(__file__).parents[2] / "records"
    else:
        RECORD_DIR_PATH = Path(user_data_dir("SincedPy"))

    RECORDS_PATH = RECORD_DIR_PATH / "data.json"
    HISORY_PATH = RECORD_DIR_PATH / "history.json"


_ctx: Context | None = None


def get_ctx() -> Context:
    global _ctx
    if _ctx is None:
        _ctx = Context()
    return _ctx
