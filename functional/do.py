from functools import wraps
from typing import Any, Callable, Generic, Protocol, cast, overload, reveal_type

from .monads.identity import Identity
from .functor import Applicative, Monad
from .monads.list import List


class Bind(Protocol):
    def __call__[A](self, __m: Monad[A]) -> A:
        ...

class Pure(Protocol):
    def __call__[A](self, __v: A) -> Monad[A]:
       ...

class NotBoundedYet[M: Monad](Exception):
    def __init__(self, m: M) -> None:
        self.m = m

def do[M: Monad, A](fn: Callable[[Bind, Pure], Monad[A]]) -> Callable[[], Monad[A]]:
    @wraps(fn)
    def run():
        def recording_fn(m: M, values: list[Any]) -> M:
            it = iter(values)
            def bind(m):
                try:
                    return next(it)
                except StopIteration:
                    raise NotBoundedYet(m)
            try:
                return fn(bind, m.pure) # type: ignore
            except NotBoundedYet as n:
                m = n.m
                return m.bind(lambda v: recording_fn(m, [*values, v]))
        res = recording_fn(cast(M, Identity(None)), [])
        return res
    return run


if __name__ == '__main__':
    from .monads.maybe import Maybe, Just, Nothing
    from .monads.list import List
    la = List.from_list([1,2]).fmap(str)
    lb = List.from_list([1,2,3])
    def compute(ma, mb):
        @do
        def body(bind: Bind, pure: Pure):
            a = bind(la)
            b = bind(lb)
            res = pure((a, b))
            return res
        return body()

    res = compute(la, lb)
