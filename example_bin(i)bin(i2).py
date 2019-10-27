# { bin(i)#bin(i+2) | i >= 0 }
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
        '0': ('q_sce#', '->'), # special case for '0#10', assuming that bin(n) starts with 1 for all n >= 1
        '1': ('q_f#', '->'),
        '#': False, # reject if starts with '#'
        '[]': False, # reject empty word
    },
    'q_sce#': { # special case, expect '#'
        '#': ('q_sce1', '->'),
        '0': False,
        '1': False,
        '[]': False,
    },
    'q_sce1': { # special case, expect 1
        '1': ('q_sce0', '->'),
        '0': False,
        '#': False,
        '[]': False,
    },
    'q_sce0': { # special case, expect 0
        '0': ('q_sce[]', '->'),
        '1': False,
        '#': False,
        '[]': False,
    },
    'q_sce[]': { # special case, expect blank
        '0': False,
        '1': False,
        '#': False,
        '[]': True,
    },
    'q_f#': { # match first '#'
        '0': '->',
        '1': '->',
        '#': ('q_fen0', '->'),
        '[]': False,
    },
    'q_fen0': { # find the end without any '0' or '#' along the way
        '0': False,
        '1': ('q_fe', '->'),
        '#': False,
        '[]': ('q_d', '<-'),
    },
    'q_fe': { # find the end without any '#' along the way
        '0': '->',
        '1': '->',
        '#': False,
        '[]': ('q_d', '<-'),
    },
    'q_d': { # decrement right number by 1 (the one after '#')
        '0': ('1', '<-'),
        '1': ('0', 'q_l', '<-'),
        '#': False,
    },
    'q_l': { # go left
        '0': '<-',
        '1': '<-',
        '#': ('q_i', '<-'),
    },
    'q_i': { # increment left number by 1 (the one before '#')
        '0': ('1', 'q_bb', '<-'),
        '1': ('0', '<-'),
        '[]': ('1', 'q_bb'),
    },
    'q_bb': { # go back to the beginning
        '0': '<-',
        '1': '<-',
        '#': '<-',
        '[]': ('q_ml', '->'),
    },
    'q_ml': { # mark first 1 from left number with '*' symbol
        '1': ('*', 'q_mrf#', '->'),
    },
    'q_mrf#': { # find first symbol after '#' symbol
        '0': '->',
        '1': '->',
        '#': ('q_mr01', '->'),
    },
    'q_mr01': { # mark first 0 or 1 with '#' symbol
        '0': ('#', 'q_mr1', '->'),
        '1': ('#', 'q_b*', '<-'),
        '[]': False,
    },
    'q_mr1': { # mark 1 with '#' symbol
        '0': False,
        '1': ('#', 'q_b*', '<-'),
        '[]': False,
    },
    'q_b*': { # go back to last '*' in left number, replacing 0s and 1s with A and B, respectively
        '0': ('A', '<-'),
        '1': ('B', '<-'),
        'A': '<-',
        'B': '<-',
        '#': '<-',
        '*': ('q_cnp', '->'),
        '[]': ('*', 'q_cnp', '->'),
    },
    'q_cnp': { # compare next pair
        'A': ('*', 'q_eA', '->'),
        'B': ('*', 'q_eB', '->'),
        '#': ('q_co#', '->'),
    },
    'q_eA': { # expect A
        'A': '->',
        'B': '->',
        '#': '->',
        '0': ('#', 'q_b*', '<-'),
        '1': False,
        '[]': False,
    },
    'q_eB': { # expect B
        'A': '->',
        'B': '->',
        '#': '->',
        '0': False,
        '1': ('#', 'q_b*', '<-'),
        '[]': False,
    },
    'q_co#': { # check if there are only '#' left
        '#': '->',
        '0': False,
        '1': False,
        '[]': True,
    },
}).test(
    itertools.chain(
        generate_words('01#', 9),
        (bin(i)[2:] + '#' + bin(i+2)[2:] for i in range(20)),
    ),
    is_correct
)
