# { bin(n)#0^n | n >= 0 }
# Tomek Zawadzki

from tmsim import *
import itertools

def is_correct(word):
    if '#' not in word:
        return False
    left, right = word.split('#', 1)
    if not left or (left[0] == '0' and left != '0') or any(map(lambda c: c != '0', right)):
        return False
    try:
        return int(left, 2) == len(right)
    except ValueError:
        return False

Algorithm({
    'q_s': {
        '0': ('q_sce#', '->'), # special case for '0#', assuming that bin(n) starts with 1 for all n >= 1
        '1': ('q_m#', '->'),
        '#': False, # reject if starts with '#'
        '[]': False, # reject empty word
    },
    'q_sce#': { # special case, expect '#'
        '0': False,
        '1': False,
        '#': ('q_sceb', '->'),
        '[]': False,
    },
    'q_sceb': { # special case, expect blank
        '0': False,
        '1': False,
        '#': False,
        '[]': True,
    },
    'q_m#': { # match first '#'
        '0': '->',
        '1': '->',
        '#': ('q_m0', '->'),
        '[]': False,
    },
    'q_m0': { # match only 0s and replace them with 2
        '0': ('2', '->'),
        '1': False,
        '#': False,
        '[]': ('q_rl2', '<-'),
    },
    'q_rl2': { # remove last '2'
        '2': ('[]', 'q_l', '<-'),
        '#': ('q_co0', '<-'),
    },
    'q_l': { # go to left side of '#'
        '2': '<-',
        '#': ('q_d', '<-'),
    },
    'q_d': { # decrement binary number
        '0': ('1', '<-'),
        '1': ('0', 'q_e', '->'),
        '[]': False, # reject if cannot decrement
    },
    'q_e': { # go to the end
        '0': '->',
        '1': '->',
        '#': '->',
        '2': '->',
        '[]': ('q_rl2', '<-'),
    },
    'q_co0': { # check if there are only 0s left
        '0': '<-',
        '1': False,
        '[]': True,
    },
}).test(
    itertools.chain(
        generate_words('01#', 9),
        (bin(n)[2:] + '#' + ('0' * n) for n in range(20)),
    ),
    is_correct
)
