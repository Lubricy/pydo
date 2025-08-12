from typing import Callable
from ..functor import Monad, A, B

class Identity(Monad[A]):
    def __init__(self, value):
        self.value = value

    @classmethod
    def pure(cls, value: B) -> 'Identity[B]':
        return Identity(value)

    def map(self, f: Callable[[A], B]) -> 'Identity[B]':
        return Identity(f(self.value))

    def bind(self, f: 'Callable[[A], Identity[B]]') -> 'Identity[B]':
        return f(self.value)

    def to_value(self) -> A:
        return self.value

    def __repr__(self) -> str:
        return f'Identity<{self.to_value()}>'

    @classmethod
    def from_value(cls, value: B) -> 'Identity[B]':
        return cls.pure(value)
