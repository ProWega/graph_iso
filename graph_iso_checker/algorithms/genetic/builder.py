from .generational        import GeneticAlgorithm
from .strategies.selection   import TournamentSelection
from .strategies.crossover   import PMXCrossover
from .strategies.mutation    import SwapMutation
from .strategies.fitness     import EdgeMatchFitness
from .strategies.termination import GenerationTermination


class GeneticAlgorithmBuilder:
    """
    Builder для конфигурации и создания GA с параллельным фитнесом.
    """
    def __init__(self):
        self._population_size = 50
        self._generations     = 200
        self._selection       = TournamentSelection()
        self._crossover       = PMXCrossover()
        self._mutation        = SwapMutation()
        self._fitness         = EdgeMatchFitness()
        self._termination     = None
        self._workers         = None


    def with_population_size(self, size: int):
        self._population_size = size
        return self


    def with_generations(self, gens: int):
        self._generations = gens
        return self


    def with_selection(self, strat):
        self._selection = strat
        return self


    def with_crossover(self, strat):
        self._crossover = strat
        return self


    def with_mutation(self, strat):
        self._mutation = strat
        return self


    def with_fitness(self, strat):
        self._fitness = strat
        return self


    def with_termination(self, strat):
        self._termination = strat
        return self


    def with_workers(self, num_workers: int):
        # число процессов для оценки фитнеса
        self._workers = num_workers
        return self


    def build(self):
        termination = self._termination or GenerationTermination(self._generations)
        return GeneticAlgorithm(
            population_size = self._population_size,
            generations     = self._generations,
            selection       = self._selection,
            crossover       = self._crossover,
            mutation        = self._mutation,
            fitness         = self._fitness,
            termination     = termination,
            num_workers     = self._workers
        )




