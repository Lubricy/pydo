from abc import abstractmethod
from typing import Protocol, Callable, Self

class Functor[*M, A](Protocol):
    def fmap[B](self, f: Callable[[A], B]) -> 'Functor[*M, B]':
        ...
    def __eq__(self, value: object, /) -> bool:
        return hash(self) == hash(value)

class Applicative[*M, A](Functor[*M, A], Protocol):
    @classmethod
    @abstractmethod
    def pure[B](cls, value: B) -> 'Applicative[*M, B]':
        ...

    # @abstractmethod
    # def ap(self, fa: 'Applicative[A]') -> Self:
    #     ...

class Monad[*M, A](Applicative[*M, A], Protocol):
    # HACK: Otherwise, Pyright thinks @do returns an Applicative,
    # thus we manually alter the return type here to compensate.
    @classmethod
    @abstractmethod
    def pure[B](cls, value: B) -> 'Monad[*M, B]':
        ...

    @abstractmethod
    def bind(self, f: Callable[[A], Self]) -> Self: # HACK: Self := Monad[*M, B]
        ...
