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