from typing import Literal, TypeVar, Callable, reveal_type

from functional.do import Bind, Pure, do
from functional.monads.free import Free, Finish, Suspend
from ..functor import Functor
from ..utils import compose
from functional import functor

# class Continuation(Functor[F]):
#     def __init__(self, next_step):
#         self.next_step = next_step

#     def fmap(self, f: Callable[[F], G]) -> 'Continuation[G]':
#         return Continuation(compose(f, self.next_step))

class ReadFile[F](Functor[F]):
    def __init__(self, path: str, next_step: Callable[[str], F]):
        self.path = path
        self.next_step = next_step

    def __repr__(self) -> str:
        return f"ReadFile('{self.path}')"
    def fmap[G](self, f: Callable[[F], G]) -> 'Functor[G]':
        return ReadFile(self.path, compose(f, self.next_step))

class WriteFile[F](Functor[F]):
    def __init__(self, path: str, content: str, next_step: Callable[[Literal[None]], F]):
        self.path = path
        self.content = content
        self.next_step = next_step

    def __repr__(self) -> str:
        return f"WriteFile('{self.path}')[{self.content}]"
    def fmap[G](self, f: Callable[[F], G]) -> 'Functor[G]':
        return WriteFile(self.path, self.content, compose(f, self.next_step))

class LogError[F](Functor[F]):
    def __init__(self, message: str, next_step: Callable[[Literal[None]], F]):
        self.message = message
        self.next_step = next_step

    def __repr__(self) -> str:
        return f"LogError('{self.message}')"

    def fmap[G](self, f: Callable[[F], G]) -> 'Functor[G]':
        return LogError(self.message, compose(f, self.next_step))

if __name__ == '__main__':
    @do
    def workflow(bind: Bind, pure: Pure):
        content = bind(Suspend(ReadFile("abdc", Finish)))
        for i in range(5):
            bind(Suspend(WriteFile(f"def{i}", content[:i], Finish)))
        return pure(len(content))

    mock_fs = {"abc": "12345"}

    def interpreter(f: Functor):
        match f:
            case ReadFile(path=path, next_step=next_step):
                content = mock_fs.get(path)
                print(path, content, next_step)
                if content:
                    return next_step(content)
                else:
                    print(f"file {path} does not exist, reading default.")
                    return Suspend(LogError(path, Finish))
            case WriteFile(path=path, content=content, next_step=next_step):
                mock_fs[path] = content
                return next_step(None)
            case LogError(message=message, next_step=next_step):
                print("Error:", message)
                return next_step(None)
            case _:
                print("this should not happen")

    def run(prog, interpreter):
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

    step = workflow()
    res = run(step, interpreter)
    print("result:", res)
    print("state", mock_fs)
