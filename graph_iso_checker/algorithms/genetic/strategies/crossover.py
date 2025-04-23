import random
from abc import ABC, abstractmethod


class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2, context):
        """
        Возвращает двух потомков (перестановки вершин).
        """
        pass


class PMXCrossover(CrossoverStrategy):
    # Partial Mapped Crossover для перестановок
    def __init__(self, crossover_rate=0.8):
        self.rate = crossover_rate


    def crossover(self, p1, p2, context):
        n = len(p1)
        # с вероятностью (1-rate) возвращаем родителей без изменений
        if random.random() > self.rate:
            return p1.copy(), p2.copy()
        # выбираем две точки
        a, b = sorted(random.sample(range(n), 2))
        # инициализируем потомков копиями
        c1, c2 = p1.copy(), p2.copy()
        # обмениваем сегменты [a:b]
        c1[a:b], c2[a:b] = p2[a:b], p1[a:b]
        # фиксируем оставшиеся позиции
        def fix(child, donor):
            for i in list(range(0, a)) + list(range(b, n)):
                val = child[i]
                while val in child[a:b]:
                    idx = donor.index(val)
                    val = child[idx]
                child[i] = val
        fix(c1, p1)
        fix(c2, p2)
        return c1, c2




