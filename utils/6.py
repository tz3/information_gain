import math
import os
import re
from collections import Counter

import numpy as np

from utils.utils import get_tokens, load_data


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
            tokens = get_tokens(self.document_name)
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
            return 1
        elif scale == 2:
            return math.log(float(self.N) / df)
        else:
            return max(0, math.log((float(self.N) - df) / df))

    def idf(self, term):
        if not term in self._idfs:
            df = self.df(term, scale=3)
            t = 0
            if df != 0:
                t = math.log(float(self.N) / df)
            self._idfs[term] = t
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

        return sorted(filter(lambda x: not np.isnan(x[0]), result), key=lambda x: x[0], reverse=True)[:10]

    def sim(self, document1, document2):
        v1 = np.array(document1.tf_idfs)
        v2 = np.array(document2.tf_idfs)
        return np.sum(v1 * v2) / (np.sqrt(np.sum(np.square(v1))) * np.sqrt(np.sum(np.square(v2))))


# t = Documents('collections')
t = Documents('documents') # 390 30889/37632 without case sensitive
# save_data(t, 'collection_6.pickle')
# t = load_data('collection_6.pickle')
# t = load_data('document_6.pickle')
query = Document('query.txt')
print t.query(query)
# print t.N, len(t.words)
# for d in t.documents:
#     print d.tf_idfs()
# save_data(t, 'task2.pickle')

# error http://stackoverflow.com/questions/27784528/numpy-division-with-runtimewarning-invalid-value-encountered-in-double-scalars
#1 [(0.077474765892289799, u'documents/written/blog/Anti-Terrorist.txt'), (0.062665494657156248, u'documents/written/newspaper:newswire/20000419_apw_eng-NEW.txt'), (0.045599478539424823, u'documents/written/letters/audubon1.txt'), (0.036316273637553083, u'documents/written/spam/ucb48.txt'), (0.031766895611634129, u'documents/written/letters/IFAW1.txt'), (0.031124014543898109, u'documents/written/letters/littleshelter2.txt'), (0.026005878539687846, u'documents/written/letters/110CYL072.txt'), (0.024558225725321754, u'documents/written/letters/110CYL070.txt'), (0.024415668370937022, u'documents/spoken/telephone/sw2014-ms98-a-trans.txt'), (0.022483740555034028, u'documents/written/letters/aspca1.txt')]
#2 [(0.15912940847418436, u'documents/written/letters/110CYL072.txt'), (0.13893299774437626, u'documents/written/letters/110CYL070.txt'), (0.091141210963060437, u'documents/written/letters/110CYL067.txt'), (0.080209996728505512, u'documents/spoken/telephone/sw2014-ms98-a-trans.txt'), (0.080005395532321583, u'documents/written/letters/110CYL068.txt'), (0.07838682324497058, u'documents/written/letters/116CUL032.txt'), (0.065411931335630655, u'documents/written/letters/118CWL050.txt'), (0.064007043422531079, u'documents/written/spam/ucb48.txt'), (0.050356152166349304, u'documents/written/letters/110CYL071.txt'), (0.049903902075576594, u'documents/written/letters/110CYL200.txt')]
#3 [(0.32730148477974441, u'documents/written/letters/110CYL072.txt'), (0.26301253601193442, u'documents/written/letters/110CYL070.txt'), (0.24343530699941451, u'documents/written/letters/110CYL067.txt'), (0.20380173570512922, u'documents/written/letters/118CWL050.txt'), (0.19466789148227864, u'documents/written/letters/110CYL068.txt'), (0.19289490436413134, u'documents/written/letters/116CUL032.txt'), (0.16769678721601397, u'documents/written/spam/ucb48.txt'), (0.15137586896461191, u'documents/written/essays/Ohio_Steel.txt'), (0.14985352696726653, u'documents/spoken/debate-transcript/3rd_Bush-Kerry.txt'), (0.14923558039951823, u'documents/written/non-fiction/CUP2.txt')]