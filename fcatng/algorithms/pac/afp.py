import math
from random import choice

from fcatng import Implication, Context
from fcatng.algorithms import closure_operators


def queries(i, epsilon, delta):
    return math.ceil(math.log(delta / i / (i+1), 1 - epsilon))


class PACBasisCalculator:
    def __init__(self, attributes, member, sample):
        self.attributes = attributes
        self.member = member
        self.sample = sample
        self.basis = []

    def calculate(self, epsilon, delta):
        i = 1
        counterexample, positive = self.find_counterexample(queries(i, epsilon, delta))
        while counterexample is not None:
            #print(len(self.basis))
            #print(counterexample, positive)
            if positive:
                self.weaken(counterexample)
            else:
                for imp in self.basis:
                    c = imp.premise & counterexample
                    if imp.premise != c and not self.member(c):
                        imp._premise = c
                        break
                else:
                    self.basis.append(Implication(counterexample, set(self.attributes)))
            i += 1
            counterexample, positive = self.find_counterexample(queries(i, epsilon, delta))

    def find_counterexample(self, k):
        print(k, len(self.basis))
        for i in range(k):
            x = self.sample()
            # print(x)
            closed = all(imp.is_respected(x) for imp in self.basis)
            if self.member(x):
                if not closed:
                    return x, True
            elif closed:
                return x, False
        return None, None

    def weaken(self, model):
        for imp in self.basis:
            if not imp.is_respected(model):
                imp._conclusion &= model


def uniform(attrs):
    return set(a for a in attrs if choice([True, False]))


ct = [[True, False, True, True],
      [True, False, True, False],
      [False, True, True, False],
      [False, True, False, True]]
objs = [1, 2, 3, 4]
attrs = ['a', 'b', 'c', 'd']
cxt = Context(ct, objs, attrs)
def is_model(x):
    return set(closure_operators.aclosure(x, cxt)) == x

calc = PACBasisCalculator(attrs, is_model, lambda: uniform(attrs))
calc.calculate(0.05, 0.05)
for i in calc.basis:
    print(i)