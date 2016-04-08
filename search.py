import os

import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

__stemmer = nltk.stem.snowball.SnowballStemmer('english')
__remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [__stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(__remove_punctuation_map)))


def cosine_sim(query, documents, tf_idf, vectorizer, top_k=5):
    query_vector = vectorizer.transform([query])
    sims = cosine_similarity(query_vector, tf_idf).flatten()
    related = sims.argsort()[:-top_k:-1]
    return sims[related], [documents[i] for i in related]


class Engine(object):
    def __init__(self, asin_path, categories_path, categories_to_asin_path, top_k=5, normilizer=normalize):
        self.top_k = top_k
        self.asin_path = asin_path
        self.categories_path = categories_path
        self.categories_to_asin_path = categories_to_asin_path
        self.categories_collection = TfidfVectorizer(tokenizer=normilizer, stop_words='english')

        docs = []
        doc_ids = os.walk(categories_path).next()[-1]
        self.__doc_ids = doc_ids
        for cat in doc_ids:
            with open(categories_path + cat, mode='r') as f:
                docs.append('\n'.join(f.readlines()))
        self.__categories_documents = docs
        self.categories_tf_idf = self.categories_collection.fit_transform(self.__categories_documents)

    def query(self, q):
        vals, category = cosine_sim(q, self.__doc_ids, self.categories_tf_idf, self.categories_collection,
                                    self.top_k)
        asin_docs = []
        asin_ids = []
        for c in category:
            with open(self.categories_to_asin_path + c, 'r') as f:
                for asin in f.readlines():
                    asin = asin.replace('\n', '')
                    asin_ids.append(asin)
                    with open(self.asin_path + asin, 'r') as asin_doc:
                        asin_docs.append(' '.join(asin_doc.readlines()))
        asin_vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
        asin_tf_idf = asin_vectorizer.fit_transform(asin_docs)
        asin_cos_sims, asins = cosine_sim(q, asin_ids, asin_tf_idf, asin_vectorizer)
        print asin_cos_sims, asins

search_engine = Engine('reviews/', 'result/', 'categories/')
while True:
    query = raw_input("\n\nquery or \q for quit\n")
    if query == '\q':
        break
    search_engine.query(query)
