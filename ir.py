import gzip
import os
from collections import defaultdict

root = '/Users/rinatahmetov/Downloads/'
meta = 'meta_Toys_and_Games.json.gz'
reviews = 'reviews_Toys_and_Games.json.gz'


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def read_by_count(file_name, k=100000):
    g = parse(file_name)
    yield [g.next() for _ in xrange(k)]


def write_to_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data + '\n')


def prepare_categories(file_name):
    g = parse(file_name)
    for _ in xrange(500):
        cat = defaultdict(list)
        for __ in xrange(1000):
            x = g.next()
            for c in x['categories'][0]:
                cat[c].append(x['asin'])
        for c in cat.keys():
            write_file("categories/%s.txt" % c, cat[c])


def prepare_reviews(file_name):
    for x in parse(file_name):
        write_to_file("reviews/%s" % x['asin'], x['reviewText'])


def write_file(file_name, data):
    with open(file_name, 'wb') as f:
        f.write('\n'.join(data))


files = os.walk('categories/').next()[-1]
for f in files:
    with open("categories/%s" % f, 'rb') as cat_f:
        for asin in cat_f.readlines():
            file_name = "reviews/%s" % asin.replace('\n', '')
            if os.path.isfile(file_name) == 1:
    			 review = open(file_name,  'rb')
    			 r = open("result/%s" % f, 'w')
    			 r.writelines(review.readlines())
    			 r.close()
    			 review.close()

# prepare_categories(root + meta)
# prepare_reviews(root + reviews)


# [write_file("result/%s" % c, reduce(lambda res, x: res + reviews[x], categories[c], [])) for c in categories.keys()]
# for c in os.walk(f)
# [write_file("result/%s" % c, reduce(lambda res, x: res + reviews[x], categories[c], [])) for c in categories.keys()]
