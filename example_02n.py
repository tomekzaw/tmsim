# { 0^(2^n) | n >= 0 }
# Tomek Zawadzki

from TuringMachine import *
import math

TuringMachine({
    'q_s': {
        '[]': False,
        '0': ('@', 'q_check_single', '->'),
    },
    'q_check_single': {
        '[]': True,
        '0': 'q_odd',
    },
    'q_even': {
        '[]': ('q_verify', '<-'),
        '0': ('q_odd', '->'),
        '#': '->',
    },
    'q_odd': {
        '[]': False,
        '0': ('#', 'q_even', '->'),
        '#': '->',
    },
    'q_verify': {
        '0': 'q_back',
        '#': '<-',
        '@': True,
    },
    'q_back': {
        '0': '<-',
        '#': '<-',
        '@': ('q_odd', '->'),
    },
}).run_tests(test_cases={
    '': False,
    **{
        '0' * n: math.log(n, 2).is_integer()
        for n in range(1, 80)
    },
})
