# Python Turing Machine Simulator
[![asciicast](https://asciinema.org/a/aJyVgDLVoFLa9xiIvUPMUBDrH.svg)](https://asciinema.org/a/aJyVgDLVoFLa9xiIvUPMUBDrH)

## Quick Start Guide
The following snippet demonstrates how to program Turing machines and check multiple test cases.
```python
from tmsim import *
import itertools

Algorithm({
    'q_s': {
        '[]': True,
        '(': ('*', 'q_r', '->'),
        ')': False,
        '*': '->',
    },
    'q_r': { # find corresponding closing bracket
        '[]': False,
        '(': '->',
        '*': '->',
        ')': ('*', 'q_b', '<-'),
    },
    'q_b': { # find opening bracket
        '*': '<-',
        '(': 'q_s',
        '[]': ('q_s', '->'),
    },
}).run('((())()(')
```

## Algorithm
When developing algorithms, you can use `<-` and `->` arrows to move the tape head one cell to the left or one cell to the right, respectively. However, you may customize behaviour of head by providing a dictionary of lambdas that accept current head position index and return new index. By default,
```python
arrows={
    '<-': lambda x: x-1,
    '->': lambda x: x+1,
}
```
which means that the tape is infinite in both directions. For left-bounded tape you may use:
```python
arrows={
    '<-': lambda x: x-1 if x > 0 else 0,
    '->': lambda x: x+1,
}
```
or equivalently:
```python
arrows={
    '<-': lambda x: max(0, x-1),
    '->': lambda x: x+1,
}
```
For finite-length tape of `size` you may use:
```python
arrows={
    '<-': lambda x: max(x-1, 0),
    '->': lambda x: min(x+1, size-1),
}
```
For one-step-right-or-jump-to-left tape you may use:
```python
arrows={
    '<-': lambda _: 0,
    '->': lambda x: x+1,
}
```

## Running
You may execute your algorithm for single input by calling `run` method on `Algorithm` object. The following code will not only instantiate a new Turing machine with given input as initial sequence and but also print all configurations one by one until machine terminates or step limit is exceeded.
```python
from tmsim import *
Algorithm({
    'q_s': {
        '0': ('1', '->'),
        '1': ('0', '->'),
        '[]': True,
    }
}).run('001011001')
```

You may also customize your simulation parameters by passing additional keyword arguments. 
The machine terminates when it reaches any state from the `result_states` dictionary keys.
Then `run` method returns dictionary value for reached state.
By default, you may use `q_y` or `True` as accepting state and `q_n` or `False` as rejecting state.
```python
result_states={
    True: True,
    False: False,
    'q_y': True,
    'q_n': False,
}
```

Not all algorithms will work on first try – some of them may fall into an infinite loop.
You may limit maximum step number by adjusting `step_limit`. You may also pass `None` to disable this feature.
When step limit is reached, an error will be raised if `raise_on_exceed` is set to `True`, otherwise `None` will be returned.
By default,
```python
step_limit=1_000_000,
raise_on_exceed=True,
```

If you need only final result, you may turn off logging by setting `print_configurations` and/or `print_result` keyword arguments.
By default,
```python
print_configurations=True,
print_result=True,
```

## Testing
You may run the test suite by calling `test` method on `Algorithm` object. This method requires two arguments: an iterable of initial sequences (tuple, list, generator etc.) and a function that returns expected output (`True`, `False`, or another value from `results_states` dictionary). Note that you may pass either lambda or name of function/method defined with `def` keyword.
```python
Algorithm({
    # write your algorithm here
}).test(
    (word for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    lambda word: word == ('0',) * (len(word)//2) + ('1',) * (len(word)//2)
)
```
