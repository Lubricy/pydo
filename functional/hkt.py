# from abc import ABC, abstractmethod
# from functools import partial
# from typing import Callable, Literal, Protocol, Self, cast, final, reveal_type, Any



# class Functor[F, T](Protocol):
#     @abstractmethod
#     def fmap[B](self, f: Callable[[T], B]) -> 'Functor[F, B]':
#         ...

# class Applicative[A, T](Functor[A, T], Protocol):
#     @classmethod
#     @abstractmethod
#     def pure[B](cls, value: B) -> 'Applicative[A, B]':
#         ...

# class Monad[M, T](Applicative[M, T], Protocol):
#     @abstractmethod
#     def bind(cls, f: Callable[[T], Self]) -> 'Self':
#         ...

# class IdentityBase[A](Monad[Literal['Identity'], A]):
#     @abstractmethod
#     def bind[B](self, f: 'Callable[[A], Identity[B]]') -> 'Identity[B]':
#         ...

# class Identity[T](IdentityBase[T]):
#     def __init__(self, value: T):
#         self.value = value
#     def fmap[B](self, f: Callable[[T], B]) -> 'Identity[B]':
#         return Identity(f(self.value))

#     @classmethod
#     def pure[B](cls, value: B) -> 'Identity[B]':
#         return Identity(value)

#     def bind[B](self, f: Callable[[T], 'Identity[B]']) -> 'Identity[B]':
#         return f(self.value)

#     def __repr__(self) -> str:
#         return f"Identity[{repr(self.value)}]"

# def fn[F, A, B](a: Functor[F, A], b: B) -> Functor[F, B]:
#     print(a.fmap)
#     return a.fmap(lambda _: b)

# i = Identity(1)
# res = fn(i, "abc")
# print(res)
