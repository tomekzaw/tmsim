# { 0^n 1^n | n >= 0 }
# Tomek Zawadzki

from tmsim import *

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
    generate_words('01', 10),
    lambda word: word == '0' * (len(word) // 2) + '1' * (len(word) // 2)
)
