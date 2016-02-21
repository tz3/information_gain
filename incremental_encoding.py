IFILE = "Cold_Mountain-Frazier_Charles.txt"
import pickle
import re


def save_data():
    tokens = []
    with open(IFILE, 'r') as f:
        lines = f.readlines()
        tokens = sorted(set(reduce(lambda res, x: res + x,
                                   map(lambda x: re.findall("\w+", x), lines), [])))
    with open('data.pickle', 'wb') as f:
        pickle.dump(tokens, f)


def load_data():
    token = []
    with open('data.pickle', 'rb') as f:
        tokens = pickle.load(f)
    return tokens


def increment_number(x):
    word = tokens[x]
    last_word = tokens[x + 1]
    for x in xrange(min(len(word), len(last_word))):
        if not last_word[x] == word[x]:
            return [x, word[x:-1]]
    return [len(last_word), word[len(last_word):-1]]

tokens = load_data()
tokens.reverse()
inc_dict = reduce(lambda res, x: res + [increment_number(x)], xrange(len(tokens)-1), [])
inc_dict += [0, tokens[-1]]
inc_dict.reverse()
print inc_dict
