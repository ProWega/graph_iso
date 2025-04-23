# graph_iso_checker/algorithms/genetic/strategies/termination.py
from abc import ABC, abstractmethod


# интерфейс стратегии останова
class TerminationStrategy(ABC):
    @abstractmethod
    # должен вернуть True, если алгоритм нужно остановить
    def should_terminate(self, population, fitnesses, generation, context):
        pass


# прекращение после заданного числа поколений
class GenerationTermination(TerminationStrategy):
    # max_gens — максимальное число поколений
    def __init__(self, max_gens):
        self.max = max_gens


    # возвращает True, если текущее поколение >= max_gens
    def should_terminate(self, population, fitnesses, generation, context):
        return generation >= self.max


# прекращение при отсутствии улучшений ("застой")
class StagnationTermination(TerminationStrategy):
    # stall_gens — число поколений без улучшения фитнеса
    def __init__(self, stall_gens):
        self.stall = stall_gens


    # возвращает True, если прошло >= stall_gens поколений с последнего улучшения
    def should_terminate(self, population, fitnesses, generation, context):
        last_imp = context.get('last_improvement', 0)
        return (generation - last_imp) >= self.stall




