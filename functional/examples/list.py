from typing import reveal_type
from functional.do import Bind, Pure, do
from functional.monads.free import Finish, Suspend
from ..monads.list import List

def execute(ma, mb):
    @do
    def prog(bind: Bind, pure: Pure):
        a = bind(ma)
        b = bind(mb)
        return pure((a, b))
    return prog()


res = execute(
    Suspend(List.from_list([1,2]).fmap(Finish)),
    Suspend(List.from_list([3,4]).fmap(Finish))
)
print(res.bind(type))
