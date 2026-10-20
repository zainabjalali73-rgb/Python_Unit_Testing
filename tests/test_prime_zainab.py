import pytest
from maths.prime_check import is_prime

ERR = "is_prime\\(\\) only accepts positive integers"


def reference_is_prime(n: int) -> bool:
    """Slow brute-force oracle used to cross-check is_prime."""
    return n > 1 and all(n % d for d in range(2, n))


# ---------- is_prime: BVA around the start of the number line ----------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "n, expected",
    [(0, False), (1, False), (2, True), (3, True), (4, False), (5, True)],
)
def test_bva_small_numbers(n, expected):
    assert is_prime(n) is expected


@pytest.mark.boundary
def test_bva_just_below_zero_raises():
    with pytest.raises(ValueError, match=ERR):
        is_prime(-1)


# ---------- is_prime: ECP valid classes ----------
@pytest.mark.unit
@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97, 563, 2999, 7919, 104729])
def test_primes_return_true(n):
    assert is_prime(n) is True


@pytest.mark.unit
@pytest.mark.parametrize("n", [4, 6, 8, 9, 15, 27, 87, 67483])
def test_composites_return_false(n):
    assert is_prime(n) is False


@pytest.mark.boundary
@pytest.mark.parametrize("n", [25, 49, 121, 169, 289])
def test_squares_of_primes_return_false(n):
    # sqrt boundary of the 6k +/- 1 loop
    assert is_prime(n) is False


@pytest.mark.unit
@pytest.mark.parametrize("n", [10, 100, 1000, 7918])
def test_even_numbers_above_two_return_false(n):
    assert is_prime(n) is False


@pytest.mark.unit
@pytest.mark.parametrize("n", [9, 21, 33, 999])
def test_odd_multiples_of_three_return_false(n):
    assert is_prime(n) is False


# ---------- is_prime: ECP invalid classes ----------
@pytest.mark.unit
@pytest.mark.parametrize("bad", [-19, -4, -1000])
def test_negative_numbers_raise(bad):
    with pytest.raises(ValueError, match=ERR):
        is_prime(bad)


@pytest.mark.unit
@pytest.mark.parametrize("bad", [16.1, 7.0, "7", None, [], (3,)])
def test_non_integer_types_raise(bad):
    with pytest.raises(ValueError, match=ERR):
        is_prime(bad)


@pytest.mark.unit
@pytest.mark.parametrize("flag, expected", [(True, False), (False, False)])
def test_bool_is_treated_as_int(flag, expected):
    # bool is a subclass of int, so True == 1 and False == 0
    assert is_prime(flag) is expected


# ---------- module-level tests ----------
@pytest.mark.unit
def test_matches_reference_for_0_to_300():
    for n in range(0, 301):
        assert is_prime(n) == reference_is_prime(n), f"mismatch at {n}"


@pytest.mark.unit
def test_there_are_25_primes_below_100():
    assert sum(is_prime(n) for n in range(100)) == 25


@pytest.mark.unit
def test_return_type_is_bool():
    assert isinstance(is_prime(7), bool)
    assert isinstance(is_prime(8), bool)