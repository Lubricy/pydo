from functools import wraps
from typing import Any, Callable, Protocol, cast, reveal_type

from .monads.identity import Identity
from .functor import A, B, Monad

class NewBind(Exception):
    def __init__(self, m: Monad) -> None:
        self.m = m

class Bind(Protocol):
    def __call__(self, __m: Monad[B]) -> B:
        ...

class Pure(Protocol):
    def __call__(self, __v: B) -> Monad[B]:
        ...

def do(fn: Callable[[Bind, Pure], Monad[A]]) -> Callable[[], Monad[A]]:
    @wraps(fn)
    def run() -> Monad[A]:
        def recording_fn(m: Monad[A], values: list[Any]) -> Monad[A]:
            it = iter(values)
            def bind(m: Monad[B]) -> B:
                try:
                    return next(it)
                except StopIteration:
                    raise NewBind(m)
            try:
                return fn(bind, m.pure)
            except NewBind as n:
                return n.m.bind(lambda v: recording_fn(n.m, [*values, v]))
        res = recording_fn(Identity(None), [])
        reveal_type(res)
        return res
    return run



if __name__ == '__main__':
    from .monads.maybe import Maybe, Just, Nothing
    from .monads.list import List
    def prog(ma, mb):
        @do
        def body(bind: Bind, pure: Pure):
            a = bind(ma)
            b = bind(mb)
            return pure((a, b))
        return body()

    la = List.from_list([1,2]).map(str)
    lb = List.from_list([1,2,3])
    ma = Just(4)
    mb: Maybe[str] = Nothing()
    res = prog(la, lb)
    reveal_type(res)
    print(res)
    res = prog(ma, mb)
    reveal_type(prog)
    reveal_type(res)
    print(res)
    #def compute(monad, ma, mb):

    # maybe = compute(Maybe, Just(3), Nothing())
    # print(maybe())
    # lst = compute(Maybe, List.from_list([1,2,3]), List.from_list([1,2,3]).map(str))
    # print(lst())
