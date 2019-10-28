# { bin(i-1)#bin(i+1) | i ∈ ℕ, i > 0}
# Tomek Zawadzki

from tmsim import *
import itertools

def is_correct(word):
    if '#' not in word:
        return False
    left, right = word.split('#', 1)
    if not left or not right or (left[0] == '0' and left != '0') or right[0] == '0' or '#' in right:
        return False
    try:
        return int(left, 2)+1 == int(right, 2)-1
    except ValueError:
        return False

Algorithm({
    'q_s': {
        '0': ('q_sce#', '->'),
        '1': ('q_f#', '->'),
        '#': False,
        '[]': False,
    },
    'q_f#': {
        '0': '->',
        '1': '->',
        '#': ('q_inc', '<-'),
        '[]': False,
    },
    'q_inc': {
        '0': ('1', 'q_r1', '->'),
        '1': ('0', '<-'),
        '[]': ('1', 'q_r1', '->'),
    },
    'q_r1': {
        '0': '->',
        '1': '->',
        '#': ('q_r2', '->'),
    },
    'q_r2': {
        '0': False,
        '1': ('q_r3', '->'),
        '#': False,
        '[]': False,
    },
    'q_r3': {
        '0': '->',
        '1': '->',
        '#': False,
        '[]': ('q_dec', '<-'),
    },
    'q_dec': {
        '0': ('1', '<-'),
        '1': ('0', 'q_b1', '<-'),
    },
    'q_b1': {
        '0': '<-',
        '1': '<-',
        '#': ('q_0#', '->'),
    },
    'q_0#': {
        '0': ('#', 'q_b2', '<-'),
        '1': ('q_b2', '<-'),
    },
    'q_b2': {
        '0': '<-',
        '1': '<-',
        '#': '<-',
        '[]': ('q_cmp', '->'),
    },
    'q_cmp': {
        '0': ('[]', 'q_m0', '->'),
        '1': ('[]', 'q_m1', '->'),
        '#': ('q_v', '->'),
    },
    'q_m0': {
        '0': '->',
        '1': '->',
        '#': ('q_e0', '->'),
    },
    'q_m1': {
        '0': '->',
        '1': '->',
        '#': ('q_e1', '->'),
    },
    'q_e0': {
        '0': ('#', 'q_b2', '<-'),
        '1': False,
        '#': '->',
        '[]': False,
    },
    'q_e1': {
        '0': False,
        '1': ('#', 'q_b2', '<-'),
        '#': '->',
        '[]': False,
    },
    'q_v': {
        '0': False,
        '1': False,
        '#': '->',
        '[]': True,
    },
    'q_sce#': {
        '0': False,
        '1': False,
        '#': ('q_sce1', '->'),
        '[]': False,
    },
    'q_sce1': {
        '0': False,
        '1': ('q_sce0', '->'),
        '#': False,
        '[]': False,
    },
    'q_sce0': {
        '0': ('q_sceb', '->'),
        '1': False,
        '#': False,
        '[]': False,
    },
    'q_sceb': {
        '0': False,
        '1': False,
        '#': False,
        '[]': True,
    },
}).test(
    itertools.chain(
        generate_words('01#', 9),
        (bin(i)[2:] + '#' + bin(i+2)[2:] for i in range(20)),
    ),
    is_correct
)
