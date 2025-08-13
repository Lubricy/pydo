from abc import abstractmethod
from typing import Protocol, Callable, Self

class Functor[A](Protocol):
    def fmap[B](self, f: Callable[[A], B]) -> 'Functor[B]':
        ...
    def __eq__(self, value: object, /) -> bool:
        return hash(self) == hash(value)

class Applicative[A](Functor[A], Protocol):
    @classmethod
    @abstractmethod
    def pure(cls, value: A) -> 'Applicative[A]':
        ...

    # @abstractmethod
    # def ap(self, fa: 'Applicative[A]') -> Self:
    #     ...

class Monad[A](Applicative[A], Protocol):
    @abstractmethod
    def bind(self, f: Callable[[A], Self]) -> Self:
        ...
