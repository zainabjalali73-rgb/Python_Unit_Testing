# Test Design Notes: Samavia

Project: TheAlgorithms/Python (fork: Python_Unit_Testing)

## Module 1: data_structures/queues/queue_by_list.py (class QueueByList)

### Equivalence Class Partitioning
| Method | Valid classes | Invalid classes |
|---|---|---|
| __init__ | None, empty, list, tuple, string, range, generator | non-iterable (int) -> TypeError |
| put | int, float, str, None, list, tuple, bool, duplicates | none |
| get | non-empty queue (FIFO) | empty queue -> IndexError |
| get_front | non-empty queue | empty queue -> IndexError |
| rotate | rotation > 0, = 0, < 0, > length | non-int -> TypeError; empty queue with rotation > 0 -> IndexError |
| __len__ / __repr__ | empty, one item, many items | none |

### Boundary Value Analysis
- Queue size: 0, 1, many (1000)
- rotate(n) with 4 items: -1, 0, 1, 3 (len-1), 4 (len), 5 (len+1), 8 (2*len)
- get / get_front: last remaining item, then empty

### Error handling
- get() on empty raises IndexError("Queue is empty")
- get_front() on empty raises IndexError (list index out of range)
- rotate(n>0) on empty raises IndexError
- QueueByList(5) raises TypeError

### Observations
- QueueByList(0) gives an empty queue because of `iterable or []`
- The constructor copies the input list, so later put() calls do not change it

### Test file: tests/test_queue_samavia.py

## Module 2: maths/factorial.py (functions factorial, factorial_recursive)

### Equivalence Class Partitioning
| Class | Examples | factorial | factorial_recursive |
|---|---|---|---|
| Non-negative integers | 0, 1, 5, 10, 25, 100 | n! | n! |
| Negative integers | -1, -10, -1000 | ValueError (negative) | ValueError (negative) |
| Non-integral floats | 0.1, 2.5, -0.5 | ValueError (integral) | ValueError (integral) |
| Integral floats | 5.0 | TypeError | ValueError (integral) |
| Negative integral floats | -5.0 | ValueError (negative) | ValueError (integral) |
| Strings | "5" | ValueError (integral) | ValueError (integral) |
| None | None | TypeError | ValueError (integral) |
| NaN / infinity | nan, inf | ValueError / OverflowError | ValueError (integral) |
| bool | True, False | 1 | 1 |

### Boundary Value Analysis
- Lower edge of valid input: -1 (error), 0, 1, 2 (results 1, 1, 2)
- Size boundary: factorial(1000) works; factorial_recursive(300) works
- Upper limit of recursion: factorial_recursive(5000) raises RecursionError

### Error handling
- Negative values: ValueError "not defined for negative values"
- Non-integral values: ValueError "only accepts integral values"

### Observations
- factorial(5.0) raises TypeError because range() rejects a float, even though the
  integral check passes
- The two functions raise different errors for the same bad input (None, 5.0, -5.0)
- True and False are accepted because bool is a subclass of int

### Module-level checks
- Both implementations agree with each other for 0..100 and with math.factorial
- n! == n * (n-1)! for n = 1..30

### Test file: tests/test_factorial_samavia.py