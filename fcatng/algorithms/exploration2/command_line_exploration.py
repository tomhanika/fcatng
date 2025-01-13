from abc import ABC, abstractmethod
from fcatng.algorithms.exploration2.exploration import Exploration, ExplorationContext, FalseCounterexample


def is_valid(imp):
    return input(f'\nIs the following implication valid:\n{imp}?\nIf not, press Enter without typing anything.\n')


class CommandLineExploration(Exploration, ABC):
    def __init__(self, cxt):
        super().__init__(ExplorationContext(cxt))
        self._session = self.create_session()

    @abstractmethod
    def get_intent(self, object_description):
        pass

    def explore(self):
        while self._session.has_open_questions():
            imp = self._session.get_open_question()
            if is_valid(imp):
                self._session.accept_implication(imp)
            else:
                counterexample = input('Provide a counterexample: ')
                intent = self.get_intent(counterexample)
                print(sorted(intent))
                try:
                    self._session.reject_implication(imp, counterexample, intent)
                except FalseCounterexample:
                    print(f'Wrong counterexample: {counterexample} satisfies the implication.')
        print("\nConfirmed implications:")
        for imp in self._session.get_accepted_implications():
            print(imp)