from abc import abstractmethod
from typing import Callable
from ..functor import Monad
# from functor import Functor

class Maybe[A](Monad[A]):
    @classmethod
    def pure(cls, value: A) -> 'Maybe[A]':
        return Just(value)

    @abstractmethod
    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        ...

class Just[A](Maybe[A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self) -> str:
        return f"Just({self.value})"

    def fmap[B](self, f: Callable[[A], B]) -> 'Maybe[B]':
        return Just(f(self.value))

    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        return f(self.value)

class Nothing[A](Maybe[A]):
    def __repr__(self) -> str:
        return f"Nothing"

    def fmap[B](self, f: Callable[[A], B]) -> 'Maybe[B]':
        return Nothing()

    def bind[B](self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        return Nothing()
