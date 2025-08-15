from typing import Callable
from functional.monads.fn import Fn


def compose[A, B, C](f: Callable[[B], C], g: Callable[[A], B]) -> Fn[A, C]:
    return Fn(g).fmap(f)
