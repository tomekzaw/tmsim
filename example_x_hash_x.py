# { x#x | x ∈ {0,1}* }
# Tomek Zawadzki

from tmsim import *

def is_correct(word):
    if '#' not in word:
        return False
    x, y = word.split('#', 1)
    return x == y

Algorithm({
    'q_s': {
        '0': ('q_r0', '[]', '->'),
        '1': ('q_r1', '[]', '->'),
        '#': ('q_c', '->'),
        '[]': False,
    },
    'q_c': {
        '0': False,
        '1': False,
        '#': False,
        '*': '->',
        '[]': True,
    },
    'q_r0': {
        '0': '->',
        '1': '->',
        '#': ('q_e0', '->'),
        '[]': False,
    },
    'q_r1': {
        '0': '->',
        '1': '->',
        '#': ('q_e1', '->'),
        '[]': False,
    },
    'q_e0': {
        '0': ('*', 'q_b', '<-'),
        '1': False,
        '#': False,
        '*': '->',
        '[]': False,
    },
    'q_e1': {
        '0': False,
        '1': ('*', 'q_b', '<-'),
        '#': False,
        '*': '->',
        '[]': False,
    },
    'q_b': {
        '0': '<-',
        '1': '<-',
        '#': '<-',
        '*': '<-',
        '[]': ('q_s', '->'),
    }
}).test(
    generate_words('01#', 9),
    is_correct
)
