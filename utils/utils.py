import os
import pickle
import re


def get_file_list(folder):
    # before need remove any .DS_Store
    return reduce(lambda res, x: res + map(
            lambda y: os.path.join(x[0], y), x[2]), os.walk(folder), [])


def get_lines(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()


def get_tokens(file_name):
    # case sensitive
    return reduce(lambda res, x: res + x,
                  map(lambda x: re.findall("\w+", x), get_lines(file_name)), [])
    # return reduce(lambda res, x: res + x,
    #               map(lambda x: map(lambda l: l.lower(), re.findall("\w+", x)), get_lines(file_name)), [])

def save_data(data, name='data.pickle'):
    with open(name, 'wb') as f:
        pickle.dump(data, f)

def save_binary(data, name="data.bin"):
    with open(name, 'wb') as f:
        for d in data:
            f.write(str(d))



def load_data(name='data.pickle'):
    with open(name, 'rb') as f:
        return pickle.load(f)
