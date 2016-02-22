import math
import os
import re
from collections import Counter

import numpy as np


def create_collection(file_name):
    if os.path.isfile(file_name) == 1:
        with open(file_name, 'r') as f:
            files = f.readlines()
            for i in range(0, len(files)):
                new_file_name = './collections/' + str(i) + '.txt'
                with open(new_file_name, 'w') as f1:
                    f1.write(files[i])


class Document:
    def __init__(self, document_name):
        self.document_name = unicode(document_name, errors='ignore')
        self._words = []
        self._counter = None
        self.length_words = 0
        self._tf_idfs = {}

    @property
    def tf_idfs(self):
        return self._tf_idfs.values()

    def tf_idf(self, term, idf):
        if not term in self._tf_idfs:
            self._tf_idfs[term] = self.tf(term) * idf
        return self._tf_idfs[term]

    @property
    def words(self):
        if not self._words:
            tokens = reduce(lambda res, x: res + x,
                            map(lambda x: re.findall("\w+", x), open(self.document_name, 'rb').readlines()), [])
            self._words = tokens
            self.length_words = len(self._words)
        return self._words

    @property
    def counter(self):
        if not self._counter:
            self._counter = Counter(self.words)
        return self._counter

    def tf(self, word):
        return self.counter[word]


class Documents(object):
    def __init__(self, folder):
        self.folder = folder
        self._words = set()
        self._tfs = None
        self._counter = None
        self._file_list = None
        self.length_words = 0
        self._documents = None
        self._idfs = {}
        self.N = 0
        self.run()

    @property
    def file_list(self):
        if not self._file_list:
            self._file_list = filter(lambda x: not x.endswith('.DS_Store'), reduce(
                    lambda res, x: res + map(lambda f: os.path.join(x[0], f), x[2]), os.walk(self.folder), []))
        self.N = len(self._file_list)
        return self._file_list

    @property
    def documents(self):
        if not self._documents:
            self._documents = [Document(x) for x in self.file_list]
        return self._documents

    def df(self, term, scale=1):
        df = len([x for x in self.documents if x.counter[term] > 0])
        if scale == 1:
            return df
        elif scale == 2:
            return math.log(float(self.N) / df)
        else:
            return max(0, math.log((float(self.N) - df) / df))

    def idf(self, term):
        if not term in self._idfs:
            self._idfs[term] = math.log(float(self.N) / self.df(term, scale=1))
        return self._idfs[term]

    def tf_idf(self, term, document):
        return document.tf_idf(term, self.idf(term))

    @property
    def words(self):
        if not self._words:
            for d in self.documents:
                self._words |= set(d.words)
        return self._words

    def run(self):
        for d in self.documents:
            for term in self.words:
                self.tf_idf(term, d)

    def query(self, q):
        for w in self.words:
            self.tf_idf(w, q)
        result = [(self.sim(d, q), d.document_name) for d in self.documents]

        return sorted(filter(lambda x: not np.isnan(x[0]), result), key=lambda x: x[0], reverse=True)

    def sim(self, document1, document2):
        v1 = np.array(document1.tf_idfs)
        v2 = np.array(document2.tf_idfs)
        return np.sum(v1 * v2) / (np.sqrt(np.sum(np.square(v1))) * np.sqrt(np.sum(np.square(v2))))


t = Documents('collections')
# t = load_data(name='task2.pickle')
query = Document('query.txt')
print t.query(query)
print t.N, len(t.words)
# for d in t.documents:
#     print d.tf_idfs()
# save_data(t, 'task2.pickle')

# error http://stackoverflow.com/questions/27784528/numpy-division-with-runtimewarning-invalid-value-encountered-in-double-scalars
