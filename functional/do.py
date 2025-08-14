from functools import wraps
from typing import Any, Callable, Concatenate, Protocol, Unpack, cast

from .functor import Monad
from .monads.identity import Identity

class Bind(Protocol):
    def __call__[*T, A](self, __m: Monad[Unpack[T], A]) -> A:
        ...

class NotBoundedYet[M: Monad](Exception):
    def __init__(self, m: M) -> None:
        self.m = m

def do[T, M:Monad, **Ps](fn: Callable[Concatenate[type[M], Bind, Ps], T]) -> Callable[Concatenate[Ps], T]:
    def run(*args: Ps.args, **kwargs: Ps.kwargs) -> T:
        def recording_fn(moand_class, values: list[Any]) -> M:
            it = iter(values)
            def bind(m):
                try:
                    return next(it)
                except StopIteration:
                    raise NotBoundedYet(m)
            try:
                return cast(M, fn(moand_class, bind, *args, **kwargs))
            except NotBoundedYet as n:
                m = n.m
                return m.bind(lambda v: recording_fn(type(m), [*values, v]))
        res = recording_fn(Identity, [])
        return cast(T, res)
    return wraps(fn)(run)


if __name__ == '__main__':
    from .monads.list import List
    la = List.from_list([1,2]).fmap(str)
    lb = List.from_list([1,2,3])

    @do
    def compute[M](m: type[Monad[M, Any]], bind: Bind, ma: Monad[M, str], mb: Monad[M, int]):
        a = bind(ma)
        b = bind(mb)
        res = m.pure((a, b))
        return res

    res = compute(la, lb)
    print(res)
