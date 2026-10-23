import pytest
from data_structures.queues.queue_by_list import QueueByList


# ---------------- __init__ ----------------
@pytest.mark.unit
def test_init_no_argument_is_empty():
    assert len(QueueByList()) == 0


@pytest.mark.unit
def test_init_none_is_empty():
    assert len(QueueByList(None)) == 0


@pytest.mark.unit
@pytest.mark.parametrize(
    "iterable, expected",
    [
        ([10, 20, 30], [10, 20, 30]),
        ((1, 2), [1, 2]),
        ("abc", ["a", "b", "c"]),
        (range(3), [0, 1, 2]),
        ((i**2 for i in range(1, 4)), [1, 4, 9]),
        ([], []),
    ],
)
def test_init_accepts_iterables(iterable, expected):
    assert QueueByList(iterable).entries == expected


@pytest.mark.unit
def test_init_non_iterable_raises():
    with pytest.raises(TypeError):
        QueueByList(5)


@pytest.mark.unit
def test_init_falsy_zero_gives_empty_queue():
    # `iterable or []` turns 0 into [] instead of raising
    assert len(QueueByList(0)) == 0


@pytest.mark.unit
def test_init_copies_input_list():
    original = [1, 2]
    q = QueueByList(original)
    q.put(3)
    assert original == [1, 2]


# ---------------- __len__ ----------------
@pytest.mark.boundary
def test_len_empty_is_zero():
    assert len(QueueByList()) == 0


@pytest.mark.boundary
def test_len_one_item():
    assert len(QueueByList([1])) == 1


@pytest.mark.unit
def test_len_after_puts_and_gets():
    q = QueueByList()
    for i in range(10):
        q.put(i)
    q.get()
    q.get()
    assert len(q) == 8


@pytest.mark.unit
def test_len_of_string_input():
    assert len(QueueByList("abcdefghijklmnopqrstuvwxyz")) == 26


# ---------------- __repr__ ----------------
@pytest.mark.unit
@pytest.mark.parametrize(
    "items, expected",
    [
        ([], "Queue(())"),
        ([10], "Queue((10,))"),
        ([10, 20, 30], "Queue((10, 20, 30))"),
        (["a", "b"], "Queue(('a', 'b'))"),
    ],
)
def test_repr(items, expected):
    assert repr(QueueByList(items)) == expected


@pytest.mark.unit
def test_str_matches_repr():
    q = QueueByList([1, 2])
    assert str(q) == repr(q)


# ---------------- put ----------------
@pytest.mark.unit
def test_put_adds_to_back():
    q = QueueByList([1])
    q.put(2)
    assert q.entries == [1, 2]


@pytest.mark.unit
def test_put_into_empty_queue():
    q = QueueByList()
    q.put("x")
    assert len(q) == 1 and q.get_front() == "x"


@pytest.mark.unit
@pytest.mark.parametrize("value", [0, -5, 3.14, "text", None, [1, 2], (3,), True])
def test_put_accepts_various_types(value):
    q = QueueByList()
    q.put(value)
    assert q.get() == value


@pytest.mark.unit
def test_put_allows_duplicates():
    q = QueueByList()
    q.put(7)
    q.put(7)
    assert len(q) == 2


@pytest.mark.boundary
def test_put_many_items_keeps_order():
    q = QueueByList()
    for i in range(1000):
        q.put(i)
    assert len(q) == 1000 and q.get() == 0 and q.get_front() == 1


# ---------------- get ----------------
@pytest.mark.unit
def test_get_returns_oldest_item_first():
    q = QueueByList([10, 20, 30])
    assert q.get() == 10


@pytest.mark.unit
def test_get_removes_item():
    q = QueueByList([10, 20])
    q.get()
    assert q.entries == [20]


@pytest.mark.boundary
def test_get_last_item_leaves_queue_empty():
    q = QueueByList([1])
    q.get()
    assert len(q) == 0


@pytest.mark.boundary
def test_get_on_empty_queue_raises():
    with pytest.raises(IndexError, match="Queue is empty"):
        QueueByList().get()


@pytest.mark.boundary
def test_get_after_emptying_raises():
    q = QueueByList([1])
    q.get()
    with pytest.raises(IndexError, match="Queue is empty"):
        q.get()


@pytest.mark.unit
def test_get_interleaved_with_put():
    q = QueueByList([10, 20, 30])
    assert q.get() == 10
    q.put(40)
    assert [q.get(), q.get(), q.get()] == [20, 30, 40]


# ---------------- rotate ----------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "rotation, expected",
    [
        (-1, [10, 20, 30, 40]),   # below 0: no change
        (0, [10, 20, 30, 40]),    # lower boundary
        (1, [20, 30, 40, 10]),
        (2, [30, 40, 10, 20]),
        (3, [40, 10, 20, 30]),    # len - 1
        (4, [10, 20, 30, 40]),    # len: full cycle
        (5, [20, 30, 40, 10]),    # len + 1: wraps
        (8, [10, 20, 30, 40]),    # two full cycles
    ],
)
def test_rotate_boundaries(rotation, expected):
    q = QueueByList([10, 20, 30, 40])
    q.rotate(rotation)
    assert q.entries == expected


@pytest.mark.unit
def test_rotate_keeps_length():
    q = QueueByList([1, 2, 3])
    q.rotate(2)
    assert len(q) == 3


@pytest.mark.unit
def test_rotate_single_item_queue_unchanged():
    q = QueueByList([9])
    q.rotate(5)
    assert q.entries == [9]


@pytest.mark.boundary
def test_rotate_zero_on_empty_queue_is_ok():
    q = QueueByList()
    q.rotate(0)
    assert len(q) == 0


@pytest.mark.boundary
def test_rotate_on_empty_queue_raises():
    with pytest.raises(IndexError):
        QueueByList().rotate(1)


@pytest.mark.unit
@pytest.mark.parametrize("bad", [1.5, "2", None])
def test_rotate_non_integer_raises(bad):
    with pytest.raises(TypeError):
        QueueByList([1, 2, 3]).rotate(bad)


# ---------------- get_front ----------------
@pytest.mark.unit
def test_get_front_returns_first_item():
    assert QueueByList([10, 20, 30]).get_front() == 10


@pytest.mark.unit
def test_get_front_does_not_remove():
    q = QueueByList([10, 20])
    q.get_front()
    assert len(q) == 2


@pytest.mark.unit
def test_get_front_after_get_moves_forward():
    q = QueueByList([10, 20, 30])
    q.get()
    assert q.get_front() == 20


@pytest.mark.boundary
def test_get_front_single_item():
    assert QueueByList([5]).get_front() == 5


@pytest.mark.boundary
def test_get_front_on_empty_queue_raises():
    with pytest.raises(IndexError):
        QueueByList().get_front()


# ---------------- class-level ----------------
@pytest.mark.unit
def test_fifo_order_end_to_end():
    q = QueueByList()
    for i in (1, 2, 3):
        q.put(i)
    assert [q.get(), q.get(), q.get()] == [1, 2, 3]


@pytest.mark.unit
def test_two_queues_are_independent():
    a, b = QueueByList(), QueueByList()
    a.put(1)
    assert len(a) == 1 and len(b) == 0


@pytest.mark.unit
def test_rotate_then_get_returns_new_front():
    q = QueueByList([1, 2, 3])
    q.rotate(1)
    assert q.get() == 2