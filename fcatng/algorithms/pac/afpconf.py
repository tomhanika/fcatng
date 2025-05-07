import math
import random

from fcatng import Implication
from fcatng.algorithms.closure_operators import *

def context_closure(s, cxt):
    return oprime(aprime(s, cxt), cxt)


def queries(i, epsilon, delta):
    return math.ceil(math.log(delta / i / (i+1), 1 - epsilon))


class PACRuleCalculator:
    def __init__(self, cxt, sample, conf, iconf=0):
        self.cxt = cxt
        self.sample = sample
        self.conf = conf
        self.iconf = iconf
        self.rules = None

    # computes a set L of rules for context K = (G, M, I) such that
    # (1) with probability >= 1 - delta, Pr(A in Mod L \ Int K) <= epsilon
    # (2) L has at most conf|G| counterexamples in G
    # (3) each implication in L has confidence at least iconf
    def calculate(self, epsilon, delta):
        self.rules = []
        i = 1
        counterexample = self.generate_counterexample(queries(i, epsilon, delta))
        while counterexample is not None:
            for imp in self.rules:
                c = imp.premise & counterexample
                if imp.premise != c:
                    if self.update_implication(imp, c):
                        break
            else:
                imp = Implication(counterexample, set(self.cxt.attributes))
                self.rules.append(imp)
                self.update_conclusion(imp) # must be successful since counterexample is not closed in the context
            i += 1
            counterexample = self.generate_counterexample(queries(i, epsilon, delta))

    def update_implication(self, imp, new_premise):
        old_premise = imp.premise.copy()
        imp._premise = new_premise
        if self.update_conclusion(imp):
            return True
        imp._premise = old_premise
        return False

    def update_conclusion(self, imp):
        # self.rules - imp is assumed to have at most conf|G| counterexamples
        old_conclusion = imp.conclusion.copy()
        counterexamples = self.find_counterexamples(self.rules)
        while (len(counterexamples) > (1-self.conf) * len(self.cxt) or
               self.compute_confidence(imp) < self.iconf):
            imp._conclusion &= random.choice(self.find_counterexamples([imp]))
            if imp.conclusion == imp.premise:
                imp._conclusion = old_conclusion
                return False
            counterexamples = self.find_counterexamples(self.rules)
        return True

    def find_counterexamples(self, rules):
        return [e for e in self.cxt.examples() if not all(r.is_respected(e) for r in rules)]

    def generate_counterexample(self, k):
        for i in range(k):
            x = self.sample()
            if all(imp.is_respected(x) for imp in self.rules) and context_closure(x, self.cxt) != x:
                return x
        return None

    def compute_confidence(self, imp):
        p, c = 0, 0
        for e in self.cxt.examples():
            if imp.premise <= e:
                p += 1
                if imp.conclusion <= e:
                    c += 1
        return c / p