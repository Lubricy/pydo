from typing import Callable
from ..functor import Monad, A, B
# from functor import Functor

class Maybe(Monad[A]):
    @classmethod
    def pure(cls, value: B) -> 'Maybe[B]':
        return Just(value)


class Just(Maybe[A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self) -> str:
        return f"Just({self.value})"

    def map(self, f: Callable[[A], B]) -> 'Maybe[B]':
        return Just(f(self.value))

    def bind(self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        return f(self.value)

class Nothing(Maybe[A]):
    def __repr__(self) -> str:
        return f"Nothing"

    def map(self, f: Callable[[A], B]) -> 'Maybe[B]':
        return Nothing()

    def bind(self, f: 'Callable[[A], Maybe[B]]') -> 'Maybe[B]':
        return Nothing()
