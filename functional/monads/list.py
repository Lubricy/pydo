from abc import abstractmethod
from typing import Callable
from ..functor import Monad, A, B
# from functor import Functor

class List(Monad[A]):
    @classmethod
    def pure(cls, value: B) -> 'List[B]':
        return Cons(value, Nil())

    @abstractmethod
    def map(self, f: Callable[[A], B]) -> 'List[B]':
        ...

    @abstractmethod
    def bind(self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        ...

    @abstractmethod
    def concat(self, other: 'List[A]') -> 'List[A]':
        ...

    @abstractmethod
    def to_list(self) -> list[A]:
        ...

    def __repr__(self) -> str:
        return f'List<{self.to_list()}>'


    @classmethod
    def from_list(cls, l: list[B]) -> 'List[B]':
        if l:
            return Cons(l[0], List.from_list(l[1:]))
        else:
            return Nil()

class Cons(List[A]):
    def __init__(self, head: A, tail: List[A]):
        self.head = head
        self.tail = tail

    def to_list(self) -> list[A]:
        return [self.head, *self.tail.to_list()]

    def map(self, f: Callable[[A], B]) -> 'List[B]':
        return Cons(f(self.head), self.tail.map(f))

    def concat(self, other: 'List[A]') -> 'List[A]':
        return Cons(self.head, self.tail.concat(other))

    def bind(self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        return f(self.head).concat(self.tail.bind(f))


class Nil(List[A]):
    def to_list(self) -> list[A]:
        return []

    def map(self, f: Callable[[A], B]) -> 'List[B]':
        return Nil()

    def concat(self, other: 'List[A]') -> 'List[A]':
        return other

    def bind(self, f: 'Callable[[A], List[B]]') -> 'List[B]':
        return Nil()
