from tmsim import *
import itertools

Algorithm({
    'q_even': {
        '0': ('q_odd', '->'),
        '1': ('q_odd', '->'),
        '[]': True,
    },
    'q_odd': {
        '0': ('q_even', '->'),
        '1': ('q_even', '->'),
        '[]': False,
    }
}, initial_state='q_even').test(
    (word for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    lambda word: len(word) % 2 == 0
)
