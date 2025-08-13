from hypothesis import given, strategies as st
from functional.monads.list import List


@given(st.builds(List.from_list, st.lists(st.text())))
def test_fmap_id(m):
    assert m.fmap(lambda x: x) == m

@given(
    st.text(),
    st.functions(
        like=lambda x: ...,
        returns=st.builds(List.from_list, st.lists(st.text())),
        pure=True))
def test_monad_left_id(v, f):
    assert List.pure(v).bind(f) == f(v)

@given(st.builds(List.from_list, st.lists(st.text())))
def test_monad_right_id(m):
    assert m.bind(List.pure) == m

@given(
    st.builds(List.from_list, st.lists(st.text())),
    st.functions(like=lambda x: ..., returns=st.text(), pure=True))
def test_monad_law(m, f):
    assert m.fmap(f) == m.bind(lambda x: List.pure(f(x)))
