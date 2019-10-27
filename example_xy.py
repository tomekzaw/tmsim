# { x#y | x jest podciągiem y }
# Tomek Zawadzki

from tmsim import *

def is_correct(word):
    if '#' not in word:
        return False
    x, y = word.split('#', 1)
    if '#' in y or len(x) > len(y):
        return False
    y = iter(y)
    try:
        for c in x:
            while c != next(y):
                pass
    except StopIteration:
        return False
    return True

Algorithm({
    'q_s': {
        '0': ('q_r0', '[]', '->'),
        '1': ('q_r1', '[]', '->'),
        '#': ('q_n#', '->'),
        '[]': False,
    },
    'q_n#': { # check if there are no '#' symbols
        '0': '->',
        '1': '->',
        '*': '->',
        '#': False,
        '[]': True,
    },
    'q_r0': { # find '#' and then match '0'
        '0': '->',
        '1': '->',
        '#': ('q_e0', '->'),
        '[]': False,
    },
    'q_r1': { # find '#' and then match '1'
        '0': '->',
        '1': '->',
        '#': ('q_e1', '->'),
        '[]': False,
    },
    'q_e0': { # found '#', expect '0'
        '0': ('*', 'q_b', '<-'),
        '1': ('*', '->'),
        '*': '->',
        '#': False,
        '[]': False,
    },
    'q_e1': { # found '#', expect '1'
        '0': ('*', '->'),
        '1': ('*', 'q_b', '<-'),
        '*': '->',
        '#': False,
        '[]': False,
    },
    'q_b': { # return to first unmatched symbol
        '0': '<-',
        '1': '<-',
        '*': '<-',
        '#': '<-',
        '[]': ('q_s', '->'),
    }
}).test(
    generate_words('01#', 9),
    is_correct
)
