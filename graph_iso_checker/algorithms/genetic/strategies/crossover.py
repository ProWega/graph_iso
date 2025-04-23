# graph_iso_checker/algorithms/genetic/strategies/crossover.py
import random
from abc import ABC, abstractmethod


class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2, context):
        """
        Возвращает двух потомков (перестановки).
        """
        pass


class PMXCrossover(CrossoverStrategy):
    # Partial Mapped Crossover для перестановок
    def __init__(self, crossover_rate=0.8):
        self.rate = crossover_rate


    def crossover(self, p1, p2, context):
        n = len(p1)
        # если очень маленький размер или не кроссируем — возвращаем копии
        if n < 2 or random.random() > self.rate:
            return p1.copy(), p2.copy()


        # выбираем точки обрезки
        a, b = sorted(random.sample(range(n), 2))


        # инициализируем потомков None
        c1 = [None] * n
        c2 = [None] * n


        # копируем сегменты
        c1[a:b] = p2[a:b]
        c2[a:b] = p1[a:b]


        # строим словари соответствий в сегменте
        mapping1 = { p1[i]: p2[i] for i in range(a, b) }  # для c2
        mapping2 = { p2[i]: p1[i] for i in range(a, b) }  # для c1


        # заполняем позиции вне сегмента
        for i in list(range(0, a)) + list(range(b, n)):
            # потомок c1: берём из p1 и «прогоняем» через mapping2
            val = p1[i]
            while val in mapping2:
                val = mapping2[val]
            c1[i] = val


            # аналогично для c2
            val = p2[i]
            while val in mapping1:
                val = mapping1[val]
            c2[i] = val

        return c1, c2




