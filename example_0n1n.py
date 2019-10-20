# { 0^n 1^n | n >= 0 }
# Tomek Zawadzki

from TuringMachine import *
import itertools

TuringMachine({
    'q_s': {
        '0': ('#', 'q_1', '->'),
        '[]': True,
        '*': ('q_c', '->'),
        '1': False,
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
}).run_tests(
    inputs=(
        word
        for length in range(0, 10+1)
        for word in itertools.product('01', repeat=length)
    ),
    expected_func=lambda word: word == ('0',) * (len(word)//2) + ('1',) * (len(word)//2)
)
