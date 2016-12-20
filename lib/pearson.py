import codecs
import sys
from math import sqrt
import os
curPath = os.path.abspath(os.curdir)
sys.path.append(curPath + '/lib')
from Recommender import Recommender

class Pearson(Recommender):
    def __init__(self, data, k=1, metric='pearson', n=5):
        super().__init__(data, k, 'pearson', n)
        self.fn = self.pearson

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * \
                      sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, user):
        recommendations = {}
        nearest = self.computeNearestNeighbor(user)
        userRatings = self.data[user]
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        for i in range(self.k):
            weight = nearest[i][1] / totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]
            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = neighborRatings[artist] * \
                                                  weight
                    else:
                        recommendations[artist] = recommendations[artist] + \
                                                  neighborRatings[artist] * \
                                                  weight
        recommendations = list(recommendations.items())[:self.n]
        recommendations = [(self.convertProductID2name(k), v)
                           for (k, v) in recommendations]
        recommendations.sort(key=lambda artistTuple: artistTuple[1],
                             reverse=True)
        return recommendations