from abc import abstractmethod
from typing import Protocol, Callable, Self, Unpack

class Functor[*M, A](Protocol):
    def fmap[B](self, f: Callable[[A], B]) -> 'Functor[Unpack[M], B]':
        ...
    def __eq__(self, value: object, /) -> bool:
        return hash(self) == hash(value)

class Applicative[*M, A](Functor[Unpack[M], A], Protocol):
    @classmethod
    @abstractmethod
    def pure[B](cls, value: B) -> 'Applicative[Unpack[M], B]':
        ...

    # @abstractmethod
    # def ap(self, fa: 'Applicative[A]') -> Self:
    #     ...

class Monad[*M, A](Applicative[Unpack[M], A], Protocol):
    @abstractmethod
    def bind(self, f: Callable[[A], Self]) -> Self: # HACK: Self := Monad[M, B]
        ...
