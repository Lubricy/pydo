from typing import Callable, TypeVar
from ..functor import Monad

class Identity[A](Monad[A]):
    B = TypeVar("B", infer_variance=True)
    def __init__(self, value: A):
        self.value = value

    @classmethod
    def pure(cls, value: A) -> 'Identity[A]':
        return Identity(value)

    def fmap[B](self, f: Callable[[A], B]) -> 'Identity[B]':
        return Identity(f(self.value))

    def bind(self, f: Callable[[A], "Identity[B]"]) -> 'Identity[B]':
        return f(self.value)

    def to_value(self) -> A:
        return self.value

    def __repr__(self) -> str:
        return f'Identity<{self.to_value()}>'

    @classmethod
    def from_value(cls, value: A) -> 'Identity[A]':
        return cls.pure(value)
