# { 0^(2^n) | n >= 0 }
# Tomek Zawadzki

from tmsim import *
import math

Algorithm({
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
}).test(
    ('0' * n for n in range(0, 80)),
    lambda word: (math.log(len(word), 2).is_integer() if len(word) else 0) and all(char == '0' for char in word)
)
