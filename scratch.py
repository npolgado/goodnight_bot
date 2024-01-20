di = {
    'jeff': {'gn': 1, 'gn2': 2, 'gn3': 3},
    'eric': {'gn': 4, 'gn2': 5, 'gn3': 6},
    'nova': {'gn': 7, 'gn2': 8, 'gn3': 9},
    'd': {'gn': 10, 'gn2': 11, 'gn3': 12},
    'e': {'gn': 13, 'gn2': 14, 'gn3': 15},
    'f': {'gn': 100, 'gn2': 0, 'gn3': 2},
}

from pprint import pprint
for k, v in di.items():
    pprint(v)
    print('---')