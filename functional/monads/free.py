from abc import abstractmethod
from typing import Callable, Literal, final

from ..functor import Functor, Monad

class Free[*Ts,  A](Monad[Literal["Free"], *Ts, A]):
    @classmethod
    def pure[B](cls, value: B) -> 'Free[ *Ts, B]':
        return Finish(value)

    @abstractmethod
    def fmap[B](self, f: Callable[[A], B]) -> 'Free[ *Ts, B]':
        ...

    @abstractmethod
    def bind[B](self, f: 'Callable[[A], Free[*Ts, B]]') -> 'Free[ *Ts, B]':
        ...

@final
class Finish[*Ts, A](Free[ *Ts, A]):
    def __init__(self, value: A):
        self.value = value

    def __repr__(self) -> str:
        return f"Finish({self.value})"

    def fmap[B](self, f: Callable[[A], B]) -> 'Free[ *Ts, B]':
        return Finish(f(self.value))

    def bind[B](self, f: 'Callable[[A], Free[ *Ts, B]]') -> 'Free[ *Ts, B]':
        return f(self.value)

    def __hash__(self):
        return hash(("Finish", self.value))

@final
class Suspend[*Ts, A](Free[*Ts, A]):
    def __init__(self, functor: Functor[*Ts, Free[*Ts, A]]):
        self.functor = functor

    def __repr__(self) -> str:
        return f"Suspend({repr(self.functor)})"

    def fmap[B](self, f: Callable[[A], B]) -> Free[ *Ts, B]:
        # return self.bind(lambda x: Finish(f(x)))
        def inner(x: Free[ *Ts, A]) -> Free[ *Ts, B]:
            return x.fmap(f)
        return Suspend(self.functor.fmap(inner))

    def bind[B](self, f: Callable[[A], Free[*Ts, B]]) -> Free[ *Ts, B]:
        return Suspend(self.functor.fmap(lambda x: x.bind(f)))

    def __hash__(self):
        return hash(("Suspend", self.functor))
