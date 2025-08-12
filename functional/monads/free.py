from abc import abstractmethod
from typing import Callable, Generic, TypeVar
from ..functor import Functor, A, B

F = TypeVar("F", bound=Functor)

class Free(Generic[F, A]):
    @classmethod
    def pure(cls, value: B) -> 'Free[F, B]':
        return Pure(value)

    @abstractmethod
    def bind(self, f: 'Callable[[A], Free[F, B]]') -> 'Free[F, B]':
        ...

class Pure(Free[F, A]):
    def __init__(self, value: A):
        self.value = value

    def bind(self, f: 'Callable[[A], Free[F, B]]') -> 'Free[F, B]':
        return f(self.value)

class Suspend(Free[F, A]):
    def __init__(self, functor: Functor[Free[F, A]]):
        self.functor = functor

    def bind(self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        return Suspend(self.functor.map(lambda x: x.bind(f)))
