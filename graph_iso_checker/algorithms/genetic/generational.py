# graph_iso_checker/algorithms/genetic/generational.py
import random
import os
import concurrent.futures
from .strategies.selection   import SelectionStrategy
from .strategies.crossover   import CrossoverStrategy
from .strategies.mutation    import MutationStrategy
from .strategies.fitness     import FitnessStrategy
from .strategies.termination import TerminationStrategy


def _eval_fitness(individual, g1, g2, fitness):
    # вспомогательная функция для параллельного расчёта фитнеса
    return fitness.evaluate(individual, g1, g2, {})


class GeneticAlgorithm:
    """
    Генетический алгоритм с параллельным расчётом фитнеса
    и использованием color refinement из контекста
    для более узкой инициализации популяции.
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
        # по умолчанию используем все логические ядра
        self.num_workers     = num_workers or os.cpu_count()


    def _initialize_population(self, g1, g2, context):
        # инициализация популяции на основе групп вершин
        # если в context есть 'colors1'/'colors2', используем их
        n = g1.num_vertices
        if 'colors1' in context and 'colors2' in context:
            groups1, groups2 = {}, {}
            for u, col in enumerate(context['colors1']):
                groups1.setdefault(col, []).append(u)
            for v, col in enumerate(context['colors2']):
                groups2.setdefault(col, []).append(v)
        else:
            # иначе группируем по степеням
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
            for key, vs1 in groups1.items():
                vs2 = groups2.get(key, [])[:]
                random.shuffle(vs2)
                for u, v in zip(vs1, vs2):
                    perm[u] = v
            population.append(perm)
        return population


    def run(self, g1, g2, context):
        # 1) Проверка числа вершин
        if g1.num_vertices != g2.num_vertices:
            return False, None
        n = g1.num_vertices


        # 2) Предварительная проверка распределения степеней
        deg1 = sorted(len(g1.neighbors(u)) for u in range(n))
        deg2 = sorted(len(g2.neighbors(u)) for u in range(n))
        if deg1 != deg2:
            return False, None


        # 3) Целевое число совпадающих рёбер
        target = context.get('edge_count')
        if target is None:
            target = sum(len(g1.neighbors(u)) for u in range(n)) // 2


        # 4) Инициализация популяции с учётом color refinement
        population = self._initialize_population(g1, g2, context)

        #print("Есть популяция!")


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
                fitnesses = [
                    self.fitness.evaluate(ind, g1, g2, context)
                    for ind in population
                ]
            #print("Оценка фитнеса готова")


            # обновление лучшей особи
            gen_best = max(fitnesses)
            idx      = fitnesses.index(gen_best)
            if gen_best > best_fit:
                best_fit = gen_best
                best_map = population[idx].copy()

            #print("Лучшая особь есть")

            print(f"gen: {generation} best: {best_fit}, target: {target}")

            # если найдено полное совпадение
            if best_fit == target:
                return True, best_map


            # проверка остановки
            if self.termination.should_terminate(population, fitnesses, generation, context):
                #print("Критерий останова")
                break

            #print("Начинаем новое поколение")
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
            #print("Готово новое поколение")




        # изоморфизм не найден
        return False, None