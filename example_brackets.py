# { x ∈ {(,)}* | x jest poprawnym nawiasowaniem }
# Tomek Zawadzki

from TuringMachine import *
import itertools

def are_brackets_balanced(word):
    if len(word) % 2 == 1:
        return False
    while True:
        next_word = str(word).replace('()', '')
        if next_word == word:
            break
        word = next_word
    return not word

TuringMachine({
    'q_s': {
        '[]': True,
        '(': ('*', 'q_r', '->'),
        ')': False,
    },
    'q_r': { # find corresponding closing bracket
        '[]': False,
        '(': '->',
        '*': '->',
        ')': ('*', 'q_b', '<-'),
    },
    'q_b': { # find opening bracket
        '*': False,
        '(': 'q_s',
    },
}).run_tests(
    inputs=(
        brackets
        for length in range(0, 12+1)
        for brackets in itertools.product('()', repeat=length)
    ),
    expected_func=are_brackets_balanced
)
