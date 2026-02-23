class Context:
    SPELLING_DISTANCE = 2


_ctx: Context | None = None


def get_ctx() -> Context:
    global _ctx
    if _ctx is None:
        _ctx = Context()
    return _ctx
