# -*- coding: utf-8 -*-
import os

from utils.utils import get_file_list, get_tokens, save_data, load_data, save_binary


class Element(object):
    def __init__(self, term, posting_lists):
        self.term = term
        self.count = 1
        self.posting_lists = set([posting_lists])

    def update(self, other):
        self.count += other.count
        self.posting_lists |= other.posting_lists

    def __str__(self):
        return "term: %s count: %d, " % (self.term, self.count) + '|'.join(str(v) for v in self.posting_lists)

    def __unicode__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.term == other.term

    def __gt__(self, other):
        return self.term.__gt__(other.term)

    def __ge__(self, other):
        return self.term.__ge__(other.term)

    def __lt__(self, other):
        return self.term.__lt__(other.term)

    def __le__(self, other):
        return self.term.__le__(other.term)


class ElementPresenter(object):
    def __init__(self, count_entrance, element):
        self.entrance = count_entrance
        self.term = element.term[count_entrance:]
        self.count = element.count
        self.posting_lists = element.posting_lists

    def __str__(self):
        return "%d, remain:%s, count:%d, " % (self.entrance, self.term, self.count) + '|'.join(str(v) for v in self.posting_lists)

    def __unicode__(self):
        return self.__str__()

def compare(term1, term2):
    c = min(len(term1), len(term2))
    for x in xrange(c):
        if not term1[x] == term2[x]:
            return x
    return c


def get_index(folder_name, force_update=False):
    index_file_name = folder_name + '.pickle'
    if not force_update and os.path.exists(index_file_name):
        return load_data(index_file_name)
    else:
        elements = []
        documents = get_file_list(folder_name)
        for doc_id in xrange(len(documents)):
            elements += map(lambda x: Element(x, doc_id), get_tokens(documents[doc_id]))
        elements.sort()
        result = []
        for el in elements:
            if result and result[-1] == el:
                result[-1].update(el)
            else:
                result.append(el)

        save_data(result, name=index_file_name)


def compress(name, k=8, force_update=False):
    result = []
    block_list = []
    elements_file_name = name + '.pickle'
    compressed_elements_file_name = name + '_compressed.pickle'
    if not force_update and os.path.exists(compressed_elements_file_name):
        return load_data(compressed_elements_file_name)
    else:
        elements = load_data(elements_file_name)
        for i in xrange(0, len(elements), k):
            block_list.append(ElementPresenter(0, elements[i]))
            last_index = len(elements) - i
            for bi in xrange(1, min(k, last_index)):
                c = compare(elements[i + bi - 1].term, elements[i + bi].term)
                block_list.append(ElementPresenter(c, elements[i + bi]))
            result.append(block_list)
            block_list = []
        save_data(result, compressed_elements_file_name)
        return result


def term_lookup(term, compressed):
    def find_block():
        def check(m):
            return term < m[0].term

        l = 0
        r = len(compressed)
        while r - l > 1:
            m = l + (r - l) // 2  # number of middle block
            if check(compressed[m]):
                r = m
            else:
                l = m
        return compressed[l]

    def find_in_block(block):
        current_word = block[0].term
        if current_word == term:
            return current_word, str(block[0])
        for el_index in xrange(1, len(block)):
            current_word = current_word[:block[el_index].entrance] + block[el_index].term
            if current_word == term:
                return current_word, str(block[el_index])
        return '', None

    return find_in_block(find_block())


def check(compressed):
    for x in compressed:
        for q in xrange(1, len(x)):
            if x[q].entrance == 0:
                return x[q]
    return None


# index = get_index('documents', force_update=False)
# print index[0]
# save_binary(index, 'index.bin')
compressed = compress('documents', 8, False)
block = compressed[255]
current_word = block[0].term
print current_word
for el_index in xrange(1, len(block)):
    current_word = current_word[:block[el_index].entrance] + block[el_index].term
    print "*%s, full_term: %s, leave: %s"% (current_word[:block[el_index].entrance], current_word, block[el_index].term)
# save_binary(compressed, 'compressed.bin')

# print check(compressed)

# print 'lookup'
print term_lookup('0019', compressed)  # found
print term_lookup('000usd', compressed)  # found
print term_lookup('01234', compressed)  # found
print term_lookup('005', compressed)  # found
print term_lookup('01H0C1LQB78Y8WWAUK', compressed)  # found
print term_lookup('012345', compressed)  # not found
