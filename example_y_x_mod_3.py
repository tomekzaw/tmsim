# { bin(x)#bin(y) | x, y >= 0, y = (x mod 3) }
# Tomek Zawadzki

from tmsim import *
import itertools

def is_correct(word):
    if '#' not in word:
        return False
    left, right = word.split('#', 1)
    if right not in ('0', '1', '10'):
        return False
    if not left or (left[0] == '0' and left != '0'):
        return False
    try:
        return int(right, 2) == int(left, 2) % 3
    except ValueError:
        return False

Algorithm({
    'q_s': {
        '0': ('q_e#0b', '->'),
        '1': ('q_f#0', '->'),
        '#': False,
        '[]': False,
    },
    'q_dec1': {
        '0': ('1', '<-'),
        '1': ('0', 'q_f#1'),
        '[]': ('q_v#0', '->'),
    },
    'q_f#1': {
        '0': '->',
        '1': '->',
        '#': ('q_dec2', '<-'),
    },
    'q_dec2': {
        '0': ('1', '<-'),
        '1': ('0', 'q_f#2'),
        '[]': ('q_v#1', '->'),
    },
    'q_f#2': {
        '0': '->',
        '1': '->',
        '#': ('q_dec3', '<-'),
    },
    'q_dec3': {
        '0': ('1', '<-'),
        '1': ('0', 'q_f#0'),
        '[]': ('q_v#10', '->'),
    },
    'q_f#0': {
        '0': '->',
        '1': '->',
        '#': ('q_dec1', '<-'),
        '[]': False,
    },
    'q_v#0': {
        '0': '->',
        '1': '->',
        '#': ('q_e0b', '->'),
    },
    'q_v#1': {
        '0': '->',
        '1': '->',
        '#': ('q_e1b', '->'),
    },
    'q_v#10': {
        '0': '->',
        '1': '->',
        '#': ('q_e10b', '->'),
    },
    'q_e#0b': {
        '0': False,
        '1': False,
        '#': ('q_e0b', '->'),
        '[]': False,
    },
    'q_e0b': {
        '0': ('q_eb', '->'),
        '1': False,
        '#': False,
        '[]': False,
    },
    'q_eb': {
        '0': False,
        '1': False,
        '#': False,
        '[]': True,
    },
    'q_e1b': {
        '0': False,
        '1': ('q_eb', '->'),
        '#': False,
        '[]': False,
    },
    'q_e10b': {
        '0': False,
        '1': ('q_e0b', '->'),
        '#': False,
        '[]': False,
    },
}).test(
    itertools.chain(
        generate_words('01#', 9),
        (bin(x)[2:] + '#' + bin(x % 3)[2:] for x in range(20)),
    ),
    is_correct
)
