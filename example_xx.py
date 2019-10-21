# { xx | x ∈ {0,1}* }
# Tomek Zawadzki

from TuringMachine import *
import itertools

TuringMachine({
    'q_s': {
        '0': ('A', 'q_r', '->'),
        '1': ('B', 'q_r', '->'),     
        'A': '->',  
        'B': '->',
        'C': ('*', 'q_C1', '<-'),
        'D': ('*', 'q_D1', '<-'),
        '[]': True,
    },
    'q_r': {
        '0': '->',
        '1': '->',
        '[]': ('q_l', '<-'),
        'C': '->',
        'D': '->',
    },
    'q_l': {
        '0': ('C', 'q_b', '<-'),
        '1': ('D', 'q_b', '<-'),
        'A': False,
        'B': False,
        'C': '<-',
        'D': '<-',
    },
    'q_b': {
        '0': '<-',
        '1': '<-',
        'A': '<-',
        'B': '<-',
        '[]': ('q_s', '->'),
    },
    'q_C1': {
        'A': '<-',
        'B': '<-',
        '[]': ('q_C2', '->'),
        '*': '<-',
    },
    'q_D1': {
        'A': '<-',
        'B': '<-',
        '[]': ('q_D2', '->'),
        '*': '<-',
    },
    'q_C2': {
        'A': ('*', 'q_*', '->'),
        'B': False,
        '*': '->',
    },
    'q_D2': {
        'A': False,
        'B': ('*', 'q_*', '->'),
        '*': '->',
    },
    'q_*': {
        'A': '->',
        'B': '->',
        'C': 'q_s',
        'D': 'q_s',
        '[]': True,
        '*': '->',
    }
}).run_tests(
    inputs=(word for length in range(0, 10+1) for word in itertools.product('01', repeat=length)),
    expected_func=lambda word: word[:len(word)//2] == word[len(word)//2:]
)
