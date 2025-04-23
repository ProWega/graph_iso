import random
import os
import concurrent.futures
from .strategies.selection   import SelectionStrategy
from .strategies.crossover   import CrossoverStrategy
from .strategies.mutation    import MutationStrategy
from .strategies.fitness     import FitnessStrategy
from .strategies.termination import TerminationStrategy


def _eval_fitness(individual, g1, g2, fitness):
    # вспомогательная функция для параллельного расчета фитнеса
    return fitness.evaluate(individual, g1, g2, {})


class GeneticAlgorithm:
    """
    Генетический алгоритм с параллельным расчетом фитнеса
    и предварительной проверкой распределения степеней.
    """
    def __init__(self,
                 population_size: int,
                 generations: int,
                 selection: SelectionStrategy,
                 crossover: CrossoverStrategy,
                 mutation: MutationStrategy,
                 fitness: FitnessStrategy,
                 termination: TerminationStrategy,
                 num_workers: int = None):
        self.population_size = population_size
        self.max_gens        = generations
        self.selection       = selection
        self.crossover       = crossover
        self.mutation        = mutation
        self.fitness         = fitness
        self.termination     = termination
        # число процессов: по умолчанию все логические ядра
        self.num_workers     = num_workers or os.cpu_count()


    def _initialize_population(self, g1, g2):
        # инициализация популяции перестановок, согласованных по степеням
        n = g1.num_vertices
        deg1 = [len(g1.neighbors(u)) for u in range(n)]
        deg2 = [len(g2.neighbors(u)) for u in range(n)]
        groups1, groups2 = {}, {}
        for u, d in enumerate(deg1):
            groups1.setdefault(d, []).append(u)
        for v, d in enumerate(deg2):
            groups2.setdefault(d, []).append(v)
        population = []
        for _ in range(self.population_size):
            perm = [None] * n
            for d, vs1 in groups1.items():
                vs2 = groups2[d][:]
                random.shuffle(vs2)
                for u, v in zip(vs1, vs2):
                    perm[u] = v
            population.append(perm)
        return population


    def run(self, g1, g2, context):
        # 1) проверка числа вершин
        n1, n2 = g1.num_vertices, g2.num_vertices
        if n1 != n2:
            return False, None
        n = n1


        # 2) проверка распределения степеней
        deg1 = sorted(len(g1.neighbors(u)) for u in range(n))
        deg2 = sorted(len(g2.neighbors(u)) for u in range(n))
        if deg1 != deg2:
            return False, None


        # 3) целевое число совпадающих рёбер (из context или вычисляем)
        target = context.get('edge_count')
        if target is None:
            target = sum(len(g1.neighbors(u)) for u in range(n)) // 2


        # 4) инициализация популяции
        population = self._initialize_population(g1, g2)


        best_map, best_fit = None, -1
        generation = 0


        while True:
            # параллельная оценка фитнеса
            if self.num_workers > 1:
                with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_workers) as exe:
                    fitnesses = list(exe.map(
                        _eval_fitness,
                        population,
                        [g1] * len(population),
                        [g2] * len(population),
                        [self.fitness] * len(population),
                    ))
            else:
                # однопоточная оценка
                fitnesses = [
                    self.fitness.evaluate(ind, g1, g2, context)
                    for ind in population
                ]


            # обновление лучшей особи
            gen_best = max(fitnesses)
            idx      = fitnesses.index(gen_best)
            if gen_best > best_fit:
                best_fit = gen_best
                best_map = population[idx].copy()


            # если найдено полное соответствие
            if best_fit == target:
                return True, best_map


            # проверка условия остановки
            if self.termination.should_terminate(population, fitnesses, generation, context):
                break


            # формирование нового поколения
            new_pop = []
            while len(new_pop) < self.population_size:
                p1, p2 = self.selection.select(population, fitnesses, context)
                c1, c2 = self.crossover.crossover(p1.copy(), p2.copy(), context)
                m1     = self.mutation.mutate(c1.copy(), context)
                m2     = self.mutation.mutate(c2.copy(), context)
                new_pop.extend([m1, m2])
            population = new_pop[:self.population_size]
            generation += 1


        # не нашли изоморфизма
        return False, None