# grammar.py

EPSILON = 'ε'

grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], [EPSILON]],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], [EPSILON]],
    'F': [['(', 'E', ')'], ['id']]
}

start_symbol = 'E'