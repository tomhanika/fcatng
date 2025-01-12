#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fcatng.algorithms.exploration2.exploration import *


def is_prime(n):
    if n == 1:
        return False

    for m in range(2, n//2 + 1):
        if n % m == 0:
            return False

    return True


def is_factorial(n):
    f = 1
    for m in range(1, n + 1):
        f *= m
        if f == n:
            return True
        if f > n:
            return False


class CommandLineExploration(Exploration):
    def __init__(self):
        self.d = {
            "even": lambda n: n % 2 == 0,
            "odd": lambda n: n % 2 == 1,
            "divisible_by_three": lambda n: n % 3 == 0,
            "prime": is_prime,
            "factorial": is_factorial
        }

        cxt = fcatng.Context(attributes=list(self.d.keys()))

        super(CommandLineExploration, self).__init__(ExplorationContext(cxt))
        self._session = self.create_session()

    def is_valid(self, imp):
        return input(f'\nIs the following implication valid:\n{imp}?\nIf not, press Enter without typing anything.\n')

    def ask_for_counterexample(self):
        return input('Provide a counterexample: ')

    def get_intent(self, number):
        return {attr for attr in self._cxt.attributes if self.d[attr](number)}

    def explore(self):
        while self._session.get_candidates():
            imp = self._session.get_candidates()[0]
            if self.is_valid(imp):
                self._session.accept_implication(imp)
            else:
                counterexample = self.ask_for_counterexample()
                intent = self.get_intent(int(counterexample))
                print(sorted(intent))
                try:
                    self._session.reject_implication(imp, counterexample, intent)
                except FalseCounterexample:
                    print(f'Wrong counterexample: {counterexample} satisfies the implication.')
        print("\nConfirmed implications:")
        for imp in self._session.get_accepted_implications():
            print(imp)



if __name__ == "__main__":
    CommandLineExploration().explore()
