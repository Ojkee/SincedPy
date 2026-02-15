from typing import Callable, Iterable


def extract_one[T](
    params: Iterable[T],
    predicate: Callable[[T], bool],
) -> tuple[T | None, list[T]]:
    rest: list[T] = []
    one: T | None = None
    for param in params:
        if one is None and predicate(param):
            one = param
        else:
            rest.append(param)

    return one, rest
