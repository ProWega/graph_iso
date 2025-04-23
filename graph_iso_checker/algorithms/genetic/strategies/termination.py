# graph_iso_checker/algorithms/genetic/strategies/termination.py
from abc import ABC, abstractmethod


class TerminationStrategy(ABC):
    @abstractmethod
    def should_terminate(self, population, fitnesses, generation, context):
        """
        Возвращает True, если генетический цикл надо остановить.
        """
        pass


class GenerationTermination(TerminationStrategy):
    # Останавливаться после заданного числа поколений
    def __init__(self, max_gens):
        self.max = max_gens


    def should_terminate(self, population, fitnesses, generation, context):
        return generation >= self.max