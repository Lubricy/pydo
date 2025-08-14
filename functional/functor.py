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
    def pure[B](cls, value: B) -> 'Applicative[B]':
        ...

    def fmap[B](self, f: Callable[[A], B]) -> 'Applicative[B]':
        ...

    # @abstractmethod
    # def ap(self, fa: 'Applicative[A]') -> Self:
    #     ...

class Monad[A](Applicative[A], Protocol):
    @classmethod
    @abstractmethod
    def pure[B](cls, value: B) -> 'Monad[B]':
        ...

    def fmap[B](self, f: Callable[[A], B]) -> 'Monad[B]':
        ...

    @abstractmethod
    def bind(self, f: Callable[[A], Self]) -> Self:
        ...
