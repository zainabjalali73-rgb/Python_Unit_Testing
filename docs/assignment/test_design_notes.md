# Test Design Notes: Zainab

Project: TheAlgorithms/Python (fork: Python_Unit_Testing)
Tools: pytest, pytest-xdist, pytest-order, pytest-cov

## Module 1: data_structures/stacks/stack.py (class Stack)

### Equivalence Class Partitioning
| Input | Valid classes | Invalid classes |
|---|---|---|
| Pushed value | int, str, None, float, list | none (any object accepted) |
| Stack state | empty, partially filled, full | n/a |
| Operation | push, pop, peek, is_empty, is_full, size, contains | n/a |

### Boundary Value Analysis (limit = 3)
- Size 0 (empty), 1, limit-1, limit, limit+1
- limit = 0 (stack is empty and full at once)

### Error handling
- pop() and peek() on an empty stack raise StackUnderflowError
- push() on a full stack raises StackOverflowError

### Test file: tests/test_stack_zainab.py (19 tests)

## Module 2: maths/prime_check.py (function is_prime)

### Equivalence Class Partitioning
| Class | Examples | Expected |
|---|---|---|
| Primes | 2, 3, 5, 97, 563, 2999, 7919, 104729 | True |
| Composites | 4, 6, 9, 15, 87, 67483 | False |
| Even numbers > 2 | 10, 100, 1000 | False |
| Odd multiples of 3 | 9, 21, 999 | False |
| Squares of primes | 25, 49, 121, 169 | False |
| Negative integers | -1, -19, -1000 | ValueError |
| Non-integers | 16.1, 7.0, "7", None, [] | ValueError |
| bool (subclass of int) | True, False | False |

### Boundary Value Analysis
- Lower edge of valid input: -1 (error), 0, 1 (not prime)
- Smallest primes: 2, 3 (True), then 4 (False), 5 (True)
- Square-root boundary of the 6k +/- 1 loop: 25, 49, 121, 169

### Error handling
- Negative numbers and non-int types raise
  ValueError("is_prime() only accepts positive integers")
- Observation: 0 is accepted although the message says "positive"

### Module-level checks
- Results agree with a brute-force reference for 0..300
- Exactly 25 primes below 100

### Test file: tests/test_prime_zainab.py