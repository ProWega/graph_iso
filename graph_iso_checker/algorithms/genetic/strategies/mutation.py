import random
from abc import ABC, abstractmethod


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, individual, context):
        """
        Модифицирует individual in-place или возвращает новый.
        """
        pass


class SwapMutation(MutationStrategy):
    # Случайный попарный обмен генов с вероятностью rate
    def __init__(self, rate=0.1):
        self.rate = rate


    def mutate(self, individual, context):
        n = len(individual)
        for i in range(n):
            if random.random() < self.rate:
                j = random.randrange(n)
                individual[i], individual[j] = individual[j], individual[i]
        return individual




