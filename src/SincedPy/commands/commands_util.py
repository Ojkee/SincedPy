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


def print_and_pick[T](iter: Iterable[T]) -> T:
    iter = list(iter)
    for i, item in enumerate(iter):
        print(i, item)
    x = int(input("pick one (enter number): "))
    if not (0 <= x < len(iter)):
        raise ValueError(f"Enter value in range 0-{len(iter)}")
    return iter[x]
