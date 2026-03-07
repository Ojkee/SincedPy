from pathlib import Path


class Context:
    SPELLING_DISTANCE = 2
    RECORD_DIR_PATH = Path(__file__).parents[2] / "records"
    RECORDS_PATH = RECORD_DIR_PATH / "data.json"


# _HISORY_PATH = _RECORDS_DIR_PATH / "history.json"


_ctx: Context | None = None


def get_ctx() -> Context:
    global _ctx
    if _ctx is None:
        _ctx = Context()
    return _ctx
