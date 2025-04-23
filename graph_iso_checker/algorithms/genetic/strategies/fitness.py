# graph_iso_checker/algorithms/genetic/strategies/fitness.py
from abc import ABC, abstractmethod


class FitnessStrategy(ABC):
    @abstractmethod
    def evaluate(self, individual, g1, g2, context):
        """
        Возвращает числовую оценку качества отображения.
        """
        pass


class EdgeMatchFitness(FitnessStrategy):
    # Фитнес — число совпадающих рёбер
    def evaluate(self, individual, g1, g2, context):
        count = 0
        n = g1.num_vertices
        for u in range(n):
            for v in g1.neighbors(u):
                if u < v and g2.has_edge(individual[u], individual[v]):
                    count += 1
        return count