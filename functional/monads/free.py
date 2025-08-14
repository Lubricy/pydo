from abc import abstractmethod
from typing import Callable

from functional.monads.identity import Identity
from ..functor import Functor, Monad

class Free[F: Functor, A](Monad[A]):
    @classmethod
    def pure[B](cls, value: B) -> 'Free[F, B]':
        return Finish(value)

    @abstractmethod
    def fmap[B](self, f: Callable[[A], B]) -> 'Free[F, B]':
        ...

    @abstractmethod
    def bind[B](self, f: 'Callable[[A], Free[F, B]]') -> 'Free[F, B]':
        ...

class Finish[F: Functor, A](Free[F, A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self) -> str:
        return f"Finish({self.value})"

    def fmap[B](self, f: Callable[[A], B]) -> 'Free[F, B]':
        return Finish(f(self.value))

    def bind[B](self, f: 'Callable[[A], Free[F, B]]') -> 'Free[F, B]':
        return f(self.value)

    def __hash__(self):
        return hash(("Finish", self.value))

class Suspend[F: Functor, A](Free[F, A]):
    def __init__(self, functor: Functor[Free[F, A]]):
        self.functor = functor

    def __repr__(self) -> str:
        return f"Suspend({self.functor})"

    def fmap[B](self, f: Callable[[A], B]) -> 'Free[F, B]':
        # return self.bind(lambda x: Finish(f(x)))
        def inner(x: Free[F, A]) -> Free[F, B]:
            return x.fmap(f)
        return Suspend(self.functor.fmap(inner))

    def bind[B](self, f: Callable[[A], Free[F, B]]) -> Free[F, B]:
        return Suspend(self.functor.fmap(lambda x: x.bind(f)))

    def __hash__(self):
        return hash(("Suspend", self.functor))
