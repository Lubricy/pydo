from abc import abstractmethod
from typing import Callable, Literal, final
from ..functor import Monad
# from functor import Functor

class Maybe[A](Monad[Literal["Maybe"], A]):
    @classmethod
    def pure[B](cls, value: B) -> 'Maybe[B]':
        return Just(value)

    @abstractmethod
    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        ...

@final
class Just[A](Maybe[A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self) -> str:
        return f"Just({self.value})"

    def fmap[B](self, f: Callable[[A], B]) -> 'Maybe[B]':
        return Just(f(self.value))

    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        return f(self.value)

@final
class Nothing[A](Maybe[A]):
    def __repr__(self) -> str:
        return f"Nothing"

    def fmap[B](self, f: Callable[[A], B]) -> 'Maybe[B]':
        del f
        return Nothing()

    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        del f
        return Nothing()
