from abc import abstractmethod
from typing import Protocol, TypeVar, Callable

A = TypeVar("A", covariant=True)
B = TypeVar("B")

class Functor(Protocol[A]):
    def map(self, f: Callable[[A], B]) -> 'Functor[B]':
        ...

class Applicative(Functor[A]):
    @classmethod
    @abstractmethod
    def pure(cls, value: B) -> 'Monad[B]':
        ...

    # @abstractmethod
    # @classmethod
    # def ap(cls, value: A) -> 'Monad[A]':
    #     ...

M = TypeVar("M", bound="Monad")
class Monad(Applicative[A]):
    @abstractmethod
    def bind(self, f: 'Callable[[A], M]') -> M:
        ...

