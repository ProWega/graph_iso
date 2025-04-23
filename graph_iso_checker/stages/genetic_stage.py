# graph_iso_checker/stages/genetic_stage.py
from ..stage import Stage, StageResult
from ..algorithms.genetic.builder import GeneticAlgorithmBuilder


class GeneticStage(Stage):
    # Этап эвристического (генетического) поиска соответствия
    def __init__(self, population_size=50, generations=200):
        self.population_size = population_size
        self.generations     = generations


    def run(self, g1, g2, context) -> StageResult:
        # Строим GA через Builder
        builder = GeneticAlgorithmBuilder() \
            .with_population_size(self.population_size) \
            .with_generations(self.generations)
        ga = builder.build()


        # Запускаем GA
        found, mapping = ga.run(g1, g2, context)
        if found:
            # если GA нашёл полное изоморфное отображение
            context['mapping'] = mapping
            context['result']  = True
            return StageResult.ISO


        # иначе продолжаем к следующему этапу
        return StageResult.CONTINUE
