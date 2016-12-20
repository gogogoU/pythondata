import codecs
import sys
from math import sqrt
import os
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/lib')
from Recommender import Recommender


class SlopeOne(Recommender):
    def genMatrixForSlopeOne(self):
        for ratings in self.data.values():
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                for (item_, ratings_) in ratings.items():
                    if item_ != item:
                        self.frequencies[item].setdefault(item_, 0)
                        self.deviations[item].setdefault(item_, 0)
                        self.frequencies[item][item_] += 1
                        self.deviations[item][item_] += (rating - ratings_)
        for (key, value) in self.deviations.items():
            for (key1, value1) in self.deviations[key].items():
                self.deviations[key][key1] /= self.frequencies[key][key1]


    def predictValueBySlopeOne(self, userRatings):
        numerator = 0
        denominator = 0
        recommender = {}
        for (nameless, rating) in userRatings.items():
            for (item, ratings) in self.deviations.items():
                if nameless in ratings  and item not in userRatings:
                    recommender.setdefault(item, {"frequencies": 0, "deviations": 0.0})
                    recommender[item]["frequencies"] += self.frequencies[item][nameless]
                    recommender[item]["deviations"] += (self.deviations[item][nameless] + userRatings[nameless]) * self.frequencies[item][nameless]

        print(recommender)
        recommenders = [(k, v["deviations"] / v["frequencies"]) for (k, v) in recommender.items()]
        print(recommenders)

