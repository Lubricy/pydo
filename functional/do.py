from functools import wraps
from typing import Any, Callable, Concatenate, Protocol, cast

from .functor import Monad


class Bind(Protocol):
    def __call__[A](self, __m: Monad[A]) -> A:
        ...

class NotBoundedYet[M: Monad](Exception):
    def __init__(self, m: M) -> None:
        self.m = m

def do[T, M:Monad, **Ps](fn: Callable[Concatenate[type[M], Bind, Ps], T]) -> Callable[Concatenate[type[M], Ps], T]:
    def run(moand_class: type[M], *args: Ps.args, **kwargs: Ps.kwargs) -> T:
        def recording_fn(values: list[Any]) -> M:
            it = iter(values)
            def bind(m):
                try:
                    return next(it)
                except StopIteration:
                    raise NotBoundedYet(m)
            try:
                return cast(M, fn(moand_class, bind, *args, **kwargs))
            except NotBoundedYet as n:
                return n.m.bind(lambda v: recording_fn([*values, v]))
        res = recording_fn([])
        return cast(T, res)
    return wraps(fn)(run)


if __name__ == '__main__':
    from .monads.list import List
    la = List.from_list([1,2]).fmap(str)
    lb = List.from_list([1,2,3])

    @do
    def compute(m: type[Monad], bind: Bind, ma: Monad[str], mb: Monad[int]):
        a = bind(ma)
        b = bind(mb)
        res = m.pure((a, b))
        return res

    res = compute(List, la, lb)
    print(res)
