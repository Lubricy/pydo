from typing import Callable, TypeVar
from functional.do import Bind, Pure, do
from functional.functor import Functor, A, B
from functional.monads.free import Finish, Free, Suspend


class Add(Functor[A]):
    def __init__(self, a: A, b: A):
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f"({self.a} + {self.b})"

    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        return Add(f(self.a), f(self.b))

class Mul(Functor[A]):
    def __init__(self, a: A, b: A):
        self.a = a
        self.b = b
    def __repr__(self) -> str:
        return f"({self.a} * {self.b})"

    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        return Add(f(self.a), f(self.b))

@do
def workflow(bind: Bind, pure: Pure):
    a = Suspend(Add(1,2))
    b = Suspend(Add(3,4))
    return pure(Finish(Mul(a, b)))



def run(prog: Free[Functor, int], interpreter):
    step = prog
    for i in range(10):
        print(step)
        match step:
            case Finish(value=value):
                return value
            case Suspend(functor=functor):
                step = interpreter(functor)
            case unexpected:
                raise ValueError(unexpected)

def interpreter(f):
    match f:
        case Add(a=a,b=b):
            Suspend(Finish(a + b))
        case Mul(a=a,b=b):
            Suspend(Finish(a * b))


step = workflow()
print(step)
#res = run(step, interpreter)
