import math

import pytest
from maths.factorial import factorial, factorial_recursive

BOTH = pytest.mark.parametrize(
    "func", [factorial, factorial_recursive], ids=["iterative", "recursive"]
)
NEG_MSG = "not defined for negative values"
INT_MSG = "only accepts integral values"


# ---------- shared behaviour: BVA around 0 and 1 ----------
@pytest.mark.boundary
@BOTH
@pytest.mark.parametrize(
    "n, expected",
    [(0, 1), (1, 1), (2, 2), (3, 6)],
)
def test_bva_smallest_inputs(func, n, expected):
    assert func(n) == expected


@pytest.mark.boundary
@BOTH
def test_bva_just_below_zero_raises(func):
    with pytest.raises(ValueError, match=NEG_MSG):
        func(-1)


# ---------- shared behaviour: ECP valid class ----------
@pytest.mark.unit
@BOTH
@pytest.mark.parametrize(
    "n, expected",
    [(4, 24), (5, 120), (6, 720), (10, 3628800), (12, 479001600)],
)
def test_known_values(func, n, expected):
    assert func(n) == expected


@pytest.mark.unit
@BOTH
@pytest.mark.parametrize("n", [20, 25, 50, 100])
def test_matches_math_factorial_for_larger_values(func, n):
    assert func(n) == math.factorial(n)


@pytest.mark.unit
@BOTH
def test_result_is_int(func):
    assert isinstance(func(5), int)


@pytest.mark.unit
@BOTH
def test_recurrence_n_times_previous(func):
    for n in range(1, 31):
        assert func(n) == n * func(n - 1)


# ---------- shared behaviour: ECP invalid classes ----------
@pytest.mark.unit
@BOTH
@pytest.mark.parametrize("n", [-1, -2, -10, -1000])
def test_negative_integers_raise(func, n):
    with pytest.raises(ValueError, match=NEG_MSG):
        func(n)


@pytest.mark.unit
@BOTH
@pytest.mark.parametrize("bad", [0.1, 2.5, -0.5, "5"])
def test_non_integral_values_raise_value_error(func, bad):
    with pytest.raises(ValueError, match=INT_MSG):
        func(bad)


@pytest.mark.unit
@BOTH
@pytest.mark.parametrize("flag, expected", [(True, 1), (False, 1)])
def test_bool_is_treated_as_int(func, flag, expected):
    assert func(flag) == expected


# ---------- factorial (iterative) only ----------
@pytest.mark.unit
def test_iterative_integral_float_raises_type_error():
    # 5.0 passes the integral check, then range(1, 6.0) fails
    with pytest.raises(TypeError):
        factorial(5.0)


@pytest.mark.unit
def test_iterative_negative_integral_float_raises_negative_error():
    with pytest.raises(ValueError, match=NEG_MSG):
        factorial(-5.0)


@pytest.mark.unit
def test_iterative_none_raises_type_error():
    with pytest.raises(TypeError):
        factorial(None)


@pytest.mark.unit
def test_iterative_nan_raises_value_error():
    with pytest.raises(ValueError):
        factorial(float("nan"))


@pytest.mark.unit
def test_iterative_infinity_raises_overflow_error():
    with pytest.raises(OverflowError):
        factorial(float("inf"))


@pytest.mark.boundary
def test_iterative_handles_large_input():
    assert factorial(1000) == math.factorial(1000)


# ---------- factorial_recursive only ----------
@pytest.mark.unit
@pytest.mark.parametrize("bad", [5.0, None, [], (3,)])
def test_recursive_non_int_types_raise_value_error(bad):
    with pytest.raises(ValueError, match=INT_MSG):
        factorial_recursive(bad)


@pytest.mark.unit
def test_recursive_negative_integral_float_raises_integral_error():
    # isinstance check runs first, so the message is about integers
    with pytest.raises(ValueError, match=INT_MSG):
        factorial_recursive(-5.0)


@pytest.mark.boundary
def test_recursive_moderate_depth_works():
    assert factorial_recursive(300) == math.factorial(300)


@pytest.mark.boundary
def test_recursive_very_large_input_hits_recursion_limit():
    with pytest.raises(RecursionError):
        factorial_recursive(5000)


# ---------- module-level checks ----------
@pytest.mark.unit
def test_both_implementations_agree_for_0_to_100():
    for n in range(101):
        assert factorial(n) == factorial_recursive(n)

import csv

def load_factorial_data():
    with open("tests/data/factorial_data.csv") as f:
        return [(int(r["n"]), int(r["expected"])) for r in csv.DictReader(f)]

@pytest.mark.data_driven
@pytest.mark.parametrize("n,expected", load_factorial_data())
def test_factorial_csv(n, expected):
    assert factorial(n) == expected