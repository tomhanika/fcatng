from . import closure_operators
from .exploration.exploration import IllegalContextModification, NotCounterexample, NotUniqueObjectName
from .. import Implication


class OrderedExploration(object):
    def __init__(self, cxt, find_counterexample, background_implications=[]):
        self.context = cxt
        self.find_counterexample = find_counterexample
        self.implications = background_implications
        self._background_size = len(background_implications)

    def accept_implication(self, impl):
        self.implications.append(impl)
        
    def reject_implication(self, impl, name, counterexample):
        if impl.is_respected(counterexample):
            raise NotCounterexample()
        if any(not i.is_respected(counterexample) for i in self.implications):
            raise IllegalContextModification()
        if name in self.context.objects:
            raise NotUniqueObjectName()
        self.context.add_object_with_intent(counterexample, name)

    @property
    def open_implications(self):
        context_closure = lambda s: set(closure_operators.aclosure(s, self.context))
        implication_closure = lambda s: closure_operators.simple_closure(s, self.implications)

        a = implication_closure(set())
        i = len(self.context.attributes)

        while len(a) < len(self.context.attributes):
            a_closed = context_closure(a)
            if a != a_closed:
                yield Implication(a.copy(), a_closed) # a_closed may change if the implication is rejected
            if (a_closed - a) & set(self.context.attributes[:i]):
                a -= set(self.context.attributes[i:])
            else:
                if len(a_closed) == len(self.context.attributes):
                    return
                a = a_closed
                i = len(self.context.attributes)
            for j in range(i-1, -1, -1):
                m = self.context.attributes[j]
                if m in a:
                    a.remove(m)
                else:
                    b = implication_closure(a | {m})
                    if not (b - a) & set(self.context.attributes[: j]):
                        a = b
                        i = j
                        break

    def run(self):
        for impl in self.open_implications:
            while impl.premise != impl.conclusion:
                name, counterexample = self.find_counterexample(impl)
                if counterexample is None:
                    self.accept_implication(impl)
                    if len(self.implications) % 100 == 0:
                        print(f'Accepted #{len(self.implications)}: {impl}')
                    break
                else:
                    try:
                        self.reject_implication(impl, name, counterexample)
                        impl._conclusion &= counterexample
                    except NotCounterexample:
                        print(f'{name}: {counterexample} is not a valid counterexample for {impl}.')
                    except IllegalContextModification:
                        print(f'{name}: {counterexample} conflicts with background knowledge or accepted implications.')
                    except NotUniqueObjectName:
                        print(f'The context already contains an object named "{name}".')
