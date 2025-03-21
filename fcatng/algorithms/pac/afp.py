import math
from random import choice

from fcatng import Implication, Context
from fcatng.algorithms import closure_operators


def queries(i, epsilon, delta):
    return math.ceil(math.log(delta / i / (i+1), 1 - epsilon))


class PACBasisCalculator:
    def __init__(self, attributes, member, sample, closure=None):
        self.attributes = attributes
        self.member = member
        self.sample = sample
        self.closure = closure
        self.basis = []

    def calculate(self, epsilon, delta, strong=False, upper=False):
        generate_counterexample = self.find_strong_counterexample if strong else self.find_counterexample
        i = 1
        counterexample, positive = generate_counterexample(queries(i, epsilon, delta))
        while counterexample is not None:
            #print(len(self.basis))
            #print(counterexample, positive)
            if positive:
                assert not upper
                self.weaken(counterexample)
            else:
                for imp in self.basis:
                    c = imp.premise & counterexample
                    if imp.premise != c and not self.member(c):
                        imp._premise = c
                        if upper:
                            imp._conclusion = self.closure(c)
                        break
                else:
                    self.basis.append(Implication(counterexample,
                                                  self.closure(counterexample)
                                                  if upper
                                                  else set(self.attributes)))
            i += 1
            counterexample, positive = generate_counterexample(queries(i, epsilon, delta))

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

    def find_strong_counterexample(self, k):
        assert self.closure is not None
        print(k, len(self.basis))
        for i in range(k):
            x = self.sample()
            actual_closure = self.closure(x)
            current_closure = closure_operators.simple_closure(x, self.basis)
            if actual_closure < current_closure:
                return actual_closure, True
            elif actual_closure != current_closure:
                # Here, we are biased towards negative counterexamples
                return current_closure, False
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