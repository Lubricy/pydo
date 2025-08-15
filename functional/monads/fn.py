from typing import Callable, Literal, final

from ..functor import Monad

@final
class Fn[I, A](Monad[Literal["Fn"], I, A]):
    def __init__(self, fn: Callable[[I], A]):
        self.fn = fn

    def __call__(self, arg: I) -> A:
        return self.fn(arg)

    def fmap[B](self, f: Callable[[A], B]) -> 'Fn[I, B]':
        return Fn(lambda x: f(self(x)))

    @classmethod
    def pure[B](cls, value: B) -> 'Fn[I, B]':
        return Fn(lambda _: value)

    def bind[B](self, f: Callable[[A], 'Fn[I, B]']) -> 'Fn[I, B]':
        return Fn(lambda i: f(self(i))(i))
