import pytest

from maths.prime_check import is_prime


@pytest.mark.order(1)
@pytest.mark.smoke
@pytest.mark.unit
def test_two_is_prime():
    assert is_prime(2)


@pytest.mark.order(2)
@pytest.mark.unit
@pytest.mark.boundary
@pytest.mark.parametrize("number", [0, 1, 4])
def test_non_primes_at_boundary(number):
    assert not is_prime(number)


@pytest.mark.order(3)
@pytest.mark.unit
@pytest.mark.parametrize(
    "number, expected",
    [(3, True), (97, True), (100, False), (7919, True)],
)
def test_general_cases(number, expected):
    assert is_prime(number) == expected


@pytest.mark.order(4)
@pytest.mark.smoke
@pytest.mark.unit
def test_last_runs_last():
    assert not is_prime(25)