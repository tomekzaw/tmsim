# Python Turing Machine Simulator

You may execute your algorithm for given initial sequence by calling `run` method on `Algorithm` object. The following code will print all Turing machine configurations one by one.
```python
from tmsim import *
Algorithm({
    'q_s': {
        '0': ('1', '->'),
        '1': ('0', '->'),
        '[]': True,
    }
})
algo.run('001011001')
```

You may also customize your simulation parameters by passing additional keyword arguments. 
The machine terminates when it reaches any state from the `result_states` dictionary keys.
Then `run` method returns dictionary value for reached state.
By default, you may use `q_y` or `True` as accepting state and `q_n` or `False` as rejecting state.
```python
result_states={True: True, False: False, 'q_y': True, 'q_n': False}
```

Not all algorithms will work on first try, some of them may fall into an infinite loop. You may limit steps number by adjusting `step_limit`. You may also pass `None` to disable this feature. When step limit is reached, an error will be raised if `raise_on_exceed` is set to `True`, otherwise `None` will be returned. By default,
```python
step_limit=1_000_000,
raise_on_exceed=True,
```

If you need only final result, you may turn off logging by setting `print_configurations` and `print_result` keyword arguments.
By default,
```python
print_configurations=True,
print_result=True,
```

## Testing
You may run the test suite by calling `test` method on `Algorithm` object. This method requires two arguments: iterable of initial sequences (tuple, list, generator etc.) and function that returns expected output (note that you may pass either lambda or any function).
```python
Algorithm({
    # write your algorithm here
}).test(
    (word for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    lambda word: word == ('0',) * (len(word)//2) + ('1',) * (len(word)//2)
)
```

## Algorithm
When developing algorithms, you can use `<-` and `->` arrows to move head one step left and one step right, respectively. By default, the tape is infinite in both directions. You may customize behaviour of head by providing a dictionary of lambdas that accept current head position and return new position.
For left-bounded tape you may use:
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
    '->': lambda x: min(x+1, 1000),
}
```
For one-step-right or jump-to-left tape you may use:
```python
arrows={
    '<-': lambda _: 0,
    '->': lambda x: x+1,
}
```
