from tmsim import *

Algorithm({
    'q_s': {
        '[]': True,
        '(': ('*', 'q_r', '->'),
        ')': False,
        '*': '->',
    },
    'q_r': { # find corresponding closing bracket
        '[]': False,
        '(': '->',
        '*': '->',
        ')': ('*', 'q_b', '<-'),
    },
    'q_b': { # find opening bracket
        '*': '<-',
        '(': 'q_s',
        '[]': ('q_s', '->'),
    },
}).run('((())()(')
