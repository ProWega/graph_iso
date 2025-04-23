import random
from abc import ABC, abstractmethod


class SelectionStrategy(ABC):
    @abstractmethod
    def select(self, population, fitnesses, context):
        """
        Возвращает двух родителей (каждый – списковая перестановка вершин).
        """
        pass


class TournamentSelection(SelectionStrategy):
    # Турнирная селекция: два независимых турнира по k участников
    def __init__(self, k=3):
        self.k = k


    def select(self, population, fitnesses, context):
        n = len(population)
        # первый турнир
        contenders = random.sample(range(n), self.k)
        best1 = max(contenders, key=lambda i: fitnesses[i])
        # второй турнир
        contenders = random.sample(range(n), self.k)
        best2 = max(contenders, key=lambda i: fitnesses[i])
        return population[best1], population[best2]




