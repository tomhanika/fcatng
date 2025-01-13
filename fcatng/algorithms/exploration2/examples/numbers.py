#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fcatng.algorithms.exploration2.command_line_exploration import CommandLineExploration
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


class NumbersExploration(CommandLineExploration):
    def __init__(self):
        self.d = {
            "even": lambda n: n % 2 == 0,
            "odd": lambda n: n % 2 == 1,
            "divisible_by_three": lambda n: n % 3 == 0,
            "prime": is_prime,
            "factorial": is_factorial
        }
        super().__init__(fcatng.Context(attributes=list(self.d.keys())))
        self._session = self.create_session()

    def get_intent(self, number):
        return {attr for attr in self._cxt.attributes if self.d[attr](int(number))}


if __name__ == "__main__":
    NumbersExploration().explore()
