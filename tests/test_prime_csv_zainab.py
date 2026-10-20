import csv
from pathlib import Path

import pytest

from maths.prime_check import is_prime

DATA_FILE = Path(__file__).parent / "data" / "prime_cases.csv"


def load_cases():
    with DATA_FILE.open(newline="") as f:
        return [
            pytest.param(
                int(row["number"]),
                row["expected"] == "True",
                id=f"{row['number']}-{row['category'].replace(' ', '_')}",
            )
            for row in csv.DictReader(f)
        ]


@pytest.mark.data_driven
@pytest.mark.parametrize("number, expected", load_cases())
def test_is_prime_from_csv(number, expected):
    assert is_prime(number) == expected