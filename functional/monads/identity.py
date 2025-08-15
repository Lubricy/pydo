from typing import Callable, Literal, final
from ..functor import Monad

@final
class Identity[A](Monad[Literal["Identity"], A]):
    def __init__(self, value: A):
        self.value = value

    @classmethod
    def pure[B](cls, value: B) -> 'Identity[B]':
        return Identity(value)

    from_value = pure

    def fmap[B](self, f: Callable[[A], B]) -> 'Identity[B]':
        return Identity(f(self.value))

    def bind[B](self, f: Callable[[A], "Identity[B]"]) -> 'Identity[B]':
        return f(self.value)

    def to_value(self) -> A:
        return self.value

    def __repr__(self) -> str:
        return f'Identity<{self.to_value()}>'

