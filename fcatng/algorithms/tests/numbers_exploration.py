from ... import Context
from ..ordered_exploration import OrderedExploration


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


predicates = {"even": lambda n: n % 2 == 0,
              "odd": lambda n: n % 2 == 1,
              "divisible_by_three": lambda n: n % 3 == 0,
              "prime": is_prime,
              "factorial": is_factorial}


def find_counterexample(impl, n):
    for i in range(1, n):
        if all(predicates[a](i) for a in impl.premise) and any(not predicates[a](i) for a in impl.conclusion):
            return str(i), set(a for a in predicates if predicates[a](i))
    return None, None


cxt = Context(attributes=list(predicates.keys()))
exploration = OrderedExploration(cxt, lambda impl: find_counterexample(impl, 100))
exploration.run()
for i in exploration.implications:
    print(i)
print(exploration.context)