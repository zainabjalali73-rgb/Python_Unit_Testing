import pytest
from data_structures.stacks.stack import (
    Stack, StackOverflowError, StackUnderflowError,
)


# ---- push: BVA on the limit (limit = 3) ----
@pytest.mark.boundary
def test_push_below_limit():
    s = Stack(limit=3)
    s.push(1); s.push(2)
    assert s.size() == 2 and not s.is_full()

@pytest.mark.boundary
def test_push_at_limit():
    s = Stack(limit=3)
    for i in range(3):
        s.push(i)
    assert s.is_full()

@pytest.mark.boundary
def test_push_over_limit_raises():
    s = Stack(limit=3)
    for i in range(3):
        s.push(i)
    with pytest.raises(StackOverflowError):
        s.push(99)

# ---- push: ECP on data types ----
@pytest.mark.unit
@pytest.mark.parametrize("value", [1, "text", None, 3.5, [1, 2]])
def test_push_accepts_various_types(value):
    s = Stack()
    s.push(value)
    assert s.peek() == value

# ---- pop ----
@pytest.mark.unit
def test_pop_returns_last_pushed():
    s = Stack(); s.push("a"); s.push("b")
    assert s.pop() == "b" and s.size() == 1

@pytest.mark.boundary
def test_pop_single_item_leaves_empty():
    s = Stack(); s.push(1); s.pop()
    assert s.is_empty()

@pytest.mark.boundary
def test_pop_empty_raises():
    with pytest.raises(StackUnderflowError):
        Stack().pop()

# ---- peek ----
@pytest.mark.unit
def test_peek_does_not_remove():
    s = Stack(); s.push(5)
    assert s.peek() == 5 and s.size() == 1

@pytest.mark.boundary
def test_peek_empty_raises():
    with pytest.raises(StackUnderflowError):
        Stack().peek()

# ---- is_empty / is_full / size ----
@pytest.mark.unit
def test_new_stack_is_empty():
    assert Stack().is_empty() and Stack().size() == 0

@pytest.mark.boundary
def test_limit_zero_is_full_and_empty():
    s = Stack(limit=0)
    assert s.is_empty() and s.is_full()

# ---- __contains__ ----
@pytest.mark.unit
@pytest.mark.parametrize("item,expected", [(1, True), (2, True), (9, False)])
def test_contains(item, expected):
    s = Stack(); s.push(1); s.push(2)
    assert (item in s) is expected

# ---- class-level behaviour ----
@pytest.mark.unit
def test_lifo_order():
    s = Stack()
    for i in (1, 2, 3):
        s.push(i)
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]