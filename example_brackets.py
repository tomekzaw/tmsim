# { x ∈ {(,)}* | x jest poprawnym nawiasowaniem }
# Tomek Zawadzki

from tmsim import *

def are_brackets_balanced(word):
    if len(word) % 2 != 0:
        return False
    count = 0
    for char in word:
        if char == '(':
            count += 1
        else:
            if count == 0:
                return False
            count -= 1
    return count == 0

"""
def are_brackets_balanced(word):
    stack = []
    for char in word:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    if stack:
        return False
    return True
"""

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
}).test(
    generate_words('()', 12),
    are_brackets_balanced
)
