# { xx | x ∈ {0,1}* }
# Tomek Zawadzki

from tmsim import *

Algorithm({
    'q_s': {
        # replace leftmost 0 or 1 with A or B, respectively
        '0': ('A', 'q_r', '->'),
        '1': ('B', 'q_r', '->'),
        # if all 0s and 1s have already been replaced and leftmost C or D is found, then start marking Cs and Ds as *
        'C': 'q_*',
        'D': 'q_*',
        # accept empty word as it meets the condition
        '[]': True,
    },
    'q_r': {
        # find rightmost 0 or 1 by finding end of the word
        '0': '->',
        '1': '->',
        # if C, D or end of the word is found, then go backwards
        'C': ('q_l', '<-'),
        'D': ('q_l', '<-'),
        '[]': ('q_l', '<-'),
    },
    'q_l': {
        # find last 0 or 1 in whole word (that has not been replaced yet) and replace with C or D, respectively
        '0': ('C', 'q_b', '<-'),
        '1': ('D', 'q_b', '<-'),
        # reject if there is no corresponding 0 or 1 left (if all 0s and 1s have already been replaced)
        'A': False,
        'B': False,
        # ignore symbols that have already been replaced (Cs and Ds)
        'C': '<-',
        'D': '<-',
    },
    'q_b': { # symbol has been replaced, go back to leftmost 0 or 1
        # ignore 0s and 1s
        '0': '<-',
        '1': '<-',
        # when rightmost A or B is found, leftmost 0 or 1 is on the right, now replace next pair
        'A': ('q_s', '->'),
        'B': ('q_s', '->'),
    },
    'q_C1': {
        # ignore As, Bs and marked Cs
        'A': '<-',
        'B': '<-',
        '*': '<-',
        # when rightmost # or left blank is found, leftmost A or B is on the right
        '#': ('q_C2', '->'),
        '[]': ('q_C2', '->'),
    },
    'q_D1': {
        # ignore As, Bs and marked Cs
        'A': '<-',
        'B': '<-',
        '*': '<-',
        # when rightmost # or left blank is found, leftmost A or B is on the right
        '#': ('q_D2', '->'),
        '[]': ('q_D2', '->'),
    },
    'q_C2': {
        # mark corresponding A as #
        'A': ('#', 'q_*', '->'),
        # reject if corresponding symbol is not A
        'B': False,
    },
    'q_D2': {
        # mark corresponding B as #
        'B': ('#', 'q_*', '->'),
        # reject if corresponding symbol is not B
        'A': False,
    },
    'q_*': { # find leftmost C or D
        # ignore As, Bs and marked Cs
        'A': '->',
        'B': '->',
        '*': '->',
        # leftmost C or D found, now replace next pair
        'C': ('*', 'q_C1', '<-'),
        'D': ('*', 'q_D1', '<-'),
        # accept if all corresponding symbols have been marked
        '[]': True,
    }
}).test(
    generate_words('01', 10),
    lambda word: len(word) % 2 == 0 and word[:len(word)//2] == word[len(word)//2:]
)
