from utils.utils import getDF
import os
import pandas as pd

class Data(object):

    def __init__(self, file_name, csv=False):
        self.file_name = file_name
        if csv:
            self.read_file(self.file_name)
        else:
            self.df = getDF(file_name)

    def find(self, asin):
        # return {'asin': '0000191639', 'description': "Three Dr. Suess' Puzzles: Green Eggs and Ham, Favorite Friends, and One Fish Two Fish Red Fish Blue Fish", 'title': 'Dr. Suess 19163 Dr. Seuss Puzzle 3 Pack Bundle', 'price': 37.12, 'salesRank': {'Toys & Games': 612379}, 'imUrl': 'http://ecx.images-amazon.com/images/I/414PLROXy-L._SY300_.jpg', 'brand': 'Dr. Seuss', 'categories': [['Toys & Games', 'Puzzles', 'Jigsaw Puzzles']]}
        # {'asin': '0005069491', 'salesRank': {'Toys & Games': 576683}, 'imUrl': 'http://ecx.images-amazon.com/images/I/51z4JDBCnAL._SY300_.jpg', 'categories': [['Toys & Games']], 'title': 'Nursery Rhymes Felt Book'},
        # {'asin': '0076561046', 'description': 'Learn Fractions Decimals Percents using flash cards.', 'title': 'Fraction Decimal Percent Card Deck', 'imUrl': 'http://ecx.images-amazon.com/images/I/51ObabPu3tL._SY300_.jpg', 'related': {'also_viewed': ['0075728680']}, 'salesRank': {'Toys & Games': 564211}, 'categories': [['Toys & Games', 'Learning & Education', 'Flash Cards']]}
        return self.df[self.df.asin == asin]

    def read_file(self, file_name):
        if os.path.isfile(file_name) == 1:
            self.df = pd.read_csv(file_name)
        return self.df

    def write_file(self, file_name):
        self.df.to_csv(file_name, index=True, header=True)


class Meta(Data):
    pass

class Reviews(Data):
    pass

# d = Data(root+meta)
# d.write_file('meta.csv')
# after them
# d = Data('meta.csv', True)
