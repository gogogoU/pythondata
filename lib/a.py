import codecs
from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }
users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}



users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
          "Lorde": 4, "Fall Out Boy": 1},
      "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
           "Lorde": 4, "Fall Out Boy": 1},
      "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
          "Lorde": 3, "Fall Out Boy": 1},
      "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
          "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
      "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
           "Daft Punk": 5, "Fall Out Boy": 3}}
class Recommender(object):
    def __init__(self, data, k = 1, metric = 'pearson', n = 5):
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson

        if type(data).__name__ == 'dict':
            self.data = data

    def convertProdctID2name(self, id):
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        print('为' + self.userid2name[id] + '计算评分')
        ratings = self.data[id]
        print('打分记录数量为: %d' % len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProdctID2name(k), v, k) for (k, v) in ratings]
        ratings.sort(key = lambda artistTuple: artistTuple[1], reverse=True)
        ratings = ratings[:n]
        for rating in ratings:
            print('评分记录:%s\t%i    %s' % (rating[0], rating[1], rating[2]))

    def loadBookDB(self, path=''):
        self.data = {}
        i = 0
        _i = 0
        f = codecs.open(path + 'ratings.csv', 'r', 'utf-8', 'ignore')
        for line in f:
            i += 1
            _i += 1
            if _i == 1:
                continue

            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()

        _i = 0
        f = codecs.open(path + 'books.csv', 'r', 'utf8', 'ignore')
        for line in f:
            i += 1
            _i += 1
            if _i == 1:
                continue
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        _i = 0
        f = codecs.open(path + 'users.csv', 'r', 'utf8', 'ignore')
        for line in f:
            i += 1
            _i += 1
            if _i == 1:
                continue
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'

            if age != 'NULL':
                value = location + '  (age:' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print(i)

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
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n))

        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return  distances

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
                if artist not in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = recommendations[artist] + (neighborRatings[artist] * weight)
        recommendations = list(recommendations.items())
        recommendations = [(self.convertProdctID2name(k),v) for (k, v) in recommendations]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return recommendations[:self.n]
    def computeSimilarity(band1, band2, userRatings):
        averages = {}
        for (key, ratings) in userRatings.items():
            averages[key] = (float(sum(ratings.items()))) / len(ratings.values())

        num = 0
        dem1 = 0
        dem2 = 0
        for (user, ratings) in userRatings.items():
            if band1 in ratings and band2 in ratings:
                avg = averages[user]
                num +=  (ratings[band1] - avg) * (ratings[band2] - avg)
                dem1 += (ratings[band1] - avg) ** 2
                dem2 += (ratings[band2] - avg) ** 2
        return num / (sqrt(dem1) * sqrt(dem2))


    def getMatrixForCos(self):
        averages = {}
        data = {}
        num = 0;
        dem1 = 0
        dem2 = 0
        for user, ratings in users3.items():
            averages[user] = float(sum(ratings.values())) / len(ratings.values())
        print(averages)
        for key, value in  users3.items():
            for key1, value1 in value.items():
                if  key1 not in self._data:
                    data[key1] = {}
                for key2, value2 in value.items():
                    if key1 != key2:
                        if key2 not in data[key1]:
                            data[key1][key2] = 0.0

        print(data)
        for key, value in data.items():
            for key1, value1 in value.items():
                num = 0
                dem1 = 0
                dem2 = 0
                for user, ratings in users3.items():
                    if key in ratings and key1 in ratings:
                        num += (ratings[key] - averages[user]) * (ratings[key1] - averages[user])
                        dem1 += (ratings[key] - averages[user]) ** 2
                        dem2 += (ratings[key1] - averages[user]) ** 2
                data[key][key1] = num / (sqrt(dem1) * sqrt(dem2))


        print(data);

    def  genMatrixForSlopeOne(self):
        for user, ratings in users2.items():
            for key, value in ratings.items():
                if key not in self._data:
                    self._data[key] = {}
                for key1, value1 in ratings.items():
                    if key1 != key:
                        if key1 not in self._data[key]:
                            self._data[key][key1] = {"fenshu": 0.0, "pingfenrenshu": 0}
                        self._data[key][key1]["fenshu"] += value - value1
                        self._data[key][key1]["pingfenrenshu"] += 1

        print(self._data)
        for key, value in self._data.items():
            for key1, value1 in value.items():
                value[key1] = value[key1]["fenshu"] / value[key1]["pingfenrenshu"]
        print(self._data)

        #for key, values in self._data.items():


r = Recommender(users)
r._data = {}
r.getMatrixForCos()


'''
r = Recommender(users)
r.loadBookDB('/Users/olddog/PycharmProjects/l1/')
print(r.recommend('171118'))
r.userRatings('171118', 5)
'''