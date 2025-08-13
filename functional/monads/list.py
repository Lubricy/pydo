from abc import abstractmethod
from typing import Callable
from ..functor import Monad

class List[A](Monad[A]):
    @classmethod
    def pure(cls, value: A) -> 'List[A]':
        return Cons(value, Nil())

    @abstractmethod
    def fmap[B](self, f: Callable[[A], B]) -> 'List[B]':
        ...

    @abstractmethod
    def bind[B](self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        ...

    @abstractmethod
    def concat(self, other: 'List[A]') -> 'List[A]':
        ...

    @abstractmethod
    def to_list(self) -> list[A]:
        ...

    def __repr__(self) -> str:
        return f'List<{self.to_list()}>'

    @abstractmethod
    def __hash__(self) -> int:
        ...

    @classmethod
    def from_list[B](cls, l: list[B]) -> 'List[B]':
        if l:
            return Cons(l[0], List.from_list(l[1:]))
        else:
            return Nil()

class Cons[A](List[A]):
    def __init__(self, head: A, tail: List[A]):
        self.head = head
        self.tail = tail

    def to_list(self) -> list[A]:
        return [self.head, *self.tail.to_list()]

    def fmap[B](self, f: Callable[[A], B]) -> 'List[B]':
        return Cons(f(self.head), self.tail.fmap(f))

    def concat(self, other: 'List[A]') -> 'List[A]':
        return Cons(self.head, self.tail.concat(other))

    def bind[B](self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        return f(self.head).concat(self.tail.bind(f))

    def __hash__(self) -> int:
        return hash((self.head, self.tail))


class Nil[A](List[A]):
    def to_list(self) -> list[A]:
        return []

    def fmap[B](self, f: Callable[[A], B]) -> 'List[B]':
        return Nil()

    def concat(self, other: 'List[A]') -> 'List[A]':
        return other

    def bind[B](self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        return Nil()

    def __hash__(self) -> int:
        return hash(None)

