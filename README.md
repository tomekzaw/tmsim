# Python Turing Machine Simulator
[![asciicast](https://asciinema.org/a/Eyi6GLepf56PSUZCJVBDoCjIM.svg)](https://asciinema.org/a/Eyi6GLepf56PSUZCJVBDoCjIM)

## Solutions
* [{ 0<sup>2<sup>*n*</sup></sup> | *n* &ge; 0 }](example_02n.py)
* [{ 0<sup>*n*</sup>1<sup>*n*</sup> | *n* &ge; 0 }](example_0n1n.py)
* [{ *xx* | *x* &isin; {0, 1}* }](example_xx.py)
* [{ *x* &isin; { (, ) }* | *x* is balanced }](example_brackets.py)

## Quick Start Guide
The following example demonstrates how to program Turing machines and verify the solution for multiple test cases.
```python
from tmsim import *
import itertools

Algorithm({
    'q_s': {
        '[]': True,
        '0': ('#', 'q_1', '->'),
        '1': False,
        '*': ('q_c', '->'),
    },
    'q_1': {
        '0': '->',
        '*': '->',
        '1': ('*', 'q_b', '<-'),
        '[]': False,
    },
    'q_b': {
        '0': '<-',
        '#': ('q_s', '->'),
        '*': '<-',
    },
    'q_c': {
        '*': '->',
        '0': False,
        '1': False,
        '[]': True,
    }
}).test(
    (''.join(word) for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    lambda word: word == '0' * (len(word) // 2) + '1' * (len(word) // 2)
)
```

## Algorithms
Formally, Turing machine is a tuple of input alphabet, tape alphabet, set of states, transition function, initial state, accepting state, rejecting state and blank symbol. By default,
* initial state (*q*<sub>s</sub>) is denoted by `q_s`, 
* accepting state (*q*<sub>y</sub>) is denoted by `q_y` or `True`,
* rejecting state (*q*<sub>n</sub>) is denoted by `q_n` or `False`,
* blank symbol (&EmptySmallSquare;) is denoted by `[]`.

The tape alphabet and the set of states are inferred from the transition function. It is also assumed that the input alphabet contains all symbols from working alphabet and does not contain blank symbol. Therefore, in most cases it is only required to define the transition function.

You may create an `Algorithm` object by passing a dictionary of dictionaries to the constructor. The keys of the outer dictionary are states, the keys of inner dictionaries are symbols, and the values of inner dictionaries represent the transition function values. For example,
```python
Algorithm({
    `q_s`: {
        '[]': True,
        '0': ('#', 'q_1', '->'),
        '1': False,
        '*': ('q_c', '->'),
    },
    ...
})
```
specifies that if `q_s` is the current state, the machine will either
* change state to `True` (accepting state), if the current symbol is `[]` (blank),
* replace current symbol with `#`, change state to `q_1`, and move one cell to the right, if the current symbol is `0`,
* change state to `False` (rejecting state), if the current symbol is `1`, or
* change state to `q_c` and move one cell to the right, if the current symbol is `*`.

Note that there is no obligation for a transition function value to be a triple of (*state*, *symbol*, *arrow*), since the missing elements will be interpreted as remaining the current state, not changing the current symbol, or not moving the tape head in this step, respectively. You may also replace tuples of single element, for instance `('->',)`, with that element itself, that is `'->'`. This trick is especially useful in case of arrows or final states.

### States
By convention, Turing machine states are strings that start with `q_`, for example `q_find`, `q_check` or `q_back`, but it is also acceptable to use abbreviations such as `q_f`, `q_c` or `q_b`, respectively, and supply additional information as comments if necessary.

### Symbols 
You may use any string as symbol, but it is advisable to use single characters as they enable passing initial sequences as strings, not tuples or lists (eg. `011` instead of `('zero', 'one', 'one')`). Good choices are `0`, `1`, `a`, `B`, `*`, `#`, `@` etc. Remember that blank symbol is denoted by `[]`.

### Arrows
When developing algorithms, you can use `<-` and `->` arrows to move the tape head one cell left or right, respectively. However, you may customize behaviour of head by providing a dictionary of lambdas that accept current head position index and return new index. By default the tape is infinite in both directions.
```python
arrows={
    '<-': lambda x: x-1,
    '->': lambda x: x+1,
}
```
For left-bounded tape you may use:
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
For finite-length tape you may use:
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

By default,
```python
blank_symbol='[]',
initial_state='q_s',      
states=(True, False),
symbols=(),
arrows={
    '<-': lambda x: x-1,
    '->': lambda x: x+1,
},
empty_word_representation='ε',
symbols_representations={'[]': '□'},  
```
Note that the sets of symbols, states and arrows must be disjoint.

## Running
You may execute your algorithm for single input by calling `run` method on `Algorithm` object. The following code will instantiate a new Turing machine with given input as initial sequence and also print all configurations one by one until machine terminates or step limit is exceeded.
```python
Algorithm({
    'q_s': {
        '0': ('1', '->'),
        '1': ('0', '->'),
        '[]': True,
    }
}).run('001011001')
```
You may also customize this behaviour by passing additional keyword arguments. The machine terminates when it reaches any state from the `final_states` dictionary keys. If that happens, `run` method returns dictionary value for reached state. By default, you may use `q_y` or `True` as accepting state and `q_n` or `False` as rejecting state.
```python
final_states={
    True: True,
    False: False,
    'q_y': True,
    'q_n': False,
}
```

Not all algorithms will work on first try &ndash; some of them may occasionally fall into an infinite loop.
You may limit maximum step number by adjusting `step_limit`. You may also pass `None` to disable this feature.
When step limit is reached, an error will be raised if `raise_on_exceed` is set to `True`, otherwise `None` will be returned. By default,
```python
step_limit=1_000_000,
raise_on_exceed=True
```

If you need only final result, you may turn off logging by setting `print_configurations` keyword argument to `False`. By default,
```python
print_configurations=True
```

## Testing
You may run the test suite by calling `test` method on `Algorithm` object. This method requires two arguments: an iterable of initial sequences (tuple, list, generator etc.) and a function that returns expected output (`True`, `False`, or another value from `results_states` dictionary). Note that you may pass either lambda or name of function/method defined with `def` keyword.
```python
Algorithm({
    # write your algorithm here
}).test(
    (''.join(word) for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    lambda word: word == '0' * (len(word) // 2) + '1' * (len(word) // 2)
)
```
