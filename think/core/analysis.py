import math


class Values:

    def __init__(self, v=None):
        self.v = v if v else []

    def add(self, d):
        self.v.append(d)
        return self

    def keep(self, start=0, step=1):
        v2 = []
        for i in range(start, len(self.v), step):
            v2.append(self.v[i])
        self.v = v2
        return self

    def get(self, i):
        return self.v[i]

    def size(self):
        return len(self.v)

    def min(self):
        if self.v:
            return min(self.v)
        else:
            return None

    def max(self):
        if self.v:
            return max(self.v)
        else:
            return None

    def sum(self):
        return sum(self.v)

    def mean(self):
        if self.v:
            return self.sum() / self.size()
        else:
            return None

    def average(self):
        return self.mean()

    def sse(self, expected=0):
        sse = 0
        for d in self.v:
            sse += (d - expected) * (d - expected)
        return sse

    def mse(self, expected=0):
        if self.v:
            return self.sse(expected) / self.size()
        else:
            return None

    def rmse(self, expected=None):
        if isinstance(expected, Values):
            if self.size() > 0 and self.size() == expected.size():
                sse = 0
                for i in range(self.size()):
                    error = self.get(i) - expected.get(i)
                    sse += error * error
                return math.sqrt(sse / self.size())
            else:
                return None
        elif expected:
            return math.sqrt(self.mse(expected))
        else:
            return None

    def nrmse(self, expected=None):
        if isinstance(expected, Values):
            if self.size() > 0 and self.size() == expected.size():
                return self.rmse(expected) / expected.mean()
            else:
                return None
        elif expected and self.v:
            return self.rmse(expected) / expected
        else:
            return None

    def sd(self):
        if self.size() > 1:
            return math.sqrt(self.sse(self.mean()) / (self.size() - 1))
        else:
            return None

    def se(self):
        if self.size() > 1:
            return self.sd() / math.sqrt(self.size())
        else:
            return None

    def ci(self):
        return 1.96 * self.se()

    def percent_over(self, threshold):
        if self.v:
            count = 0
            for d in self.v:
                if d > threshold:
                    count += 1
            return 100 * count / self.size()
        else:
            return None

    def r(self, values):
        if self.size() > 0 and self.size() == values.size():
            m1 = self.mean()
            m2 = values.mean()
            sd1 = self.sd()
            sd2 = values.sd()
            res = 0
            for i in range(self.size()):
                res += (self.get(i) - m1) * (values.get(i) - m2)
            return res / ((self.size() - 1) * sd1 * sd2)
        else:
            return None

    def tab_string(self, places=3):
        vals = map(lambda d: ('{:.' + str(places) + 'f}').format(d), self.v)
        return '\t'.join(vals)

    def __str__(self, places=3):
        vals = map(lambda d: ('{:.' + str(places) + 'f}').format(d), self.v)
        return '[' + ', '.join(vals) + ']'


class Data:

    def __init__(self, size):
        self.values_list = [Values() for _ in range(size)]

    def add(self, i, d):
        self.values_list[i].add(d)

    def means(self):
        res = Values()
        for values in self.values_list:
            m = values.mean()
            res.add(m if m else 0)
        return res

    def analyze(self, human):
        return Result(self.means(), human)


class Result:

    def __init__(self, model, human):
        if isinstance(human, list):
            human = Values(human)
        self.model = model
        self.human = human
        self.r = model.r(human)
        self.rmse = model.rmse(human)
        self.nrmse = model.nrmse(human)

    def output(self, title, places=2, labels=None):
        if not labels:
            labels = range(1, self.model.size() + 1)
        print('\n' + title + '\n\t' + '\t'.join(str(x) for x in labels))
        print('Human\t' + self.human.tab_string(places))
        print('Model\t' + self.model.tab_string(places))
        print('** R = {:.2f}'.format(self.r))
        print('** RMSE = {:.2f}'.format(self.rmse))
        print('** NRMSE = {:.2f}'.format(self.nrmse))
