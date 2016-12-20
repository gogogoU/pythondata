import codecs
import sys
from math import sqrt
import os
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/lib')
from Recommender import Recommender

class Cosin(Recommender):


    def genCosinForMatrix(self):
        averages = {}
        userRatings = self.data
        for (user, ratings) in userRatings.items():
            averages[user] = float(sum(ratings.values())) / len(ratings.values())

        for (user, ratings) in userRatings.items():
            for (item1, rating) in ratings.items():
                self.deviations.setdefault(item1, {})
                for (item2, someone) in ratings.items():
                    if item1 != item2:
                        self.deviations[item1].setdefault(item2, {"num": 0.0, "dem1": 0.0, "dem2": 0.0})
                        if item1 in ratings and item2 in ratings:
                            self.deviations[item1][item2]["num"] += ((ratings[item1] - averages[user]) * (ratings[item2] - averages[user]))
                            self.deviations[item1][item2]["dem1"] += ((ratings[item1] - averages[user]) ** 2)
                            self.deviations[item1][item2]["dem2"] += ((ratings[item2] - averages[user]) ** 2)
        for (item1, ratings) in self.deviations.items():
            for (item2, rating) in ratings.items():
                self.deviations[item1][item2] =  self.deviations[item1][item2]["num"] / (sqrt(self.deviations[item1][item2]["dem1"])  * sqrt(self.deviations[item1][item2]["dem2"]))
        print(self.deviations)
    def predictValueByCosin(self, userRatings):
        numerator = 0
        denominator = 0
        #print(self.deviations)
        recommender = {}
        for (nameless, rating) in userRatings.items():
            for (item, ratings) in self.deviations.items():
                if nameless in ratings  and item not in userRatings:
                    recommender.setdefault(item, {"numerator": 0, "denominator": 0})
                    recommender[item]["numerator"] += (self.deviations[item][nameless] * self.normalization(rating, 5, 1))
                    recommender[item]["denominator"] += abs(self.deviations[item][nameless])
        print(recommender)
        for (key, value) in recommender.items():
            recommender[key] =  self.unnormalization(recommender[key]["numerator"] / recommender[key]["denominator"], 5, 1)
        print(recommender)
