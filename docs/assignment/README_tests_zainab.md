# Test execution guide (Zainab)

Run all commands from the repo root with the venv active.

## My test files
- tests/test_stack_zainab.py (stack.py)
- tests/test_prime_zainab.py and tests/test_prime_csv_zainab.py (prime_check.py)
- tests/test_task4_zainab.py (markers, ordering, suites)
- Data file: tests/data/prime_cases.csv

## Configuration
Markers are registered in pyproject.toml under [tool.pytest]: unit, boundary, data_driven, smoke.
Plugins: pytest-xdist (parallel), pytest-order (ordering), pytest-cov (coverage).

## Parallel execution
pytest tests/test_stack_zainab.py tests/test_prime_zainab.py tests/test_prime_csv_zainab.py tests/test_task4_zainab.py -n auto

## Test groups / suites
- Smoke suite: pytest tests/test_task4_zainab.py -m smoke
- Unit without boundary: pytest tests/test_task4_zainab.py -m "unit and not boundary"
- Boundary only: pytest tests/test_task4_zainab.py -m boundary
- Data-driven (CSV): pytest tests/test_prime_csv_zainab.py -m data_driven

## Parameterization
@pytest.mark.parametrize is used in test_task4_zainab.py, test_stack_zainab.py,
and test_prime_csv_zainab.py (inputs loaded from CSV).

## Execution order
@pytest.mark.order(n) in test_task4_zainab.py. Run without -n to see the order.

## Coverage
pytest tests/test_stack_zainab.py --cov=data_structures.stacks.stack --cov-report=term-missing