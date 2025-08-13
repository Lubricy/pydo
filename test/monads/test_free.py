from hypothesis import given, strategies as st
from functional.monads.free import Suspend, Finish, Free
from functional.monads.list import List

monad_strategy = st.recursive(
    st.builds(Finish, st.text()),
    lambda b: st.builds(lambda x: Suspend(List.pure(x)), b))

@given(monad_strategy)
def test_fmap_id(m):
    assert m.fmap(lambda x: x) == m

@given(
    monad_strategy,
    st.functions(
        like=lambda x: ...,
        returns=monad_strategy,
        pure=True))
def test_monad_left_id(v, f):
    assert Free.pure(v).bind(f) == f(v)

@given(monad_strategy)
def test_monad_right_id(m):
    assert m.bind(Free.pure) == m

@given(monad_strategy,
       st.functions(
        like=lambda x: ...,
        returns=monad_strategy,
        pure=True))
def test_monad_right_id2(m, f):
    assert m.bind(lambda x: Free.pure(f(x))) == m.fmap(f)

# @given(
#     st.builds(List.from_list, st.lists(st.text())),
#     st.functions(like=lambda x: ..., returns=st.text(), pure=True))
# def test_monad_law(m, f):
#     assert m.fmap(f) == m.bind(lambda x: List.pure(f(x)))
